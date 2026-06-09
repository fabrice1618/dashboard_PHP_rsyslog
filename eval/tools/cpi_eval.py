#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outillage reproductible pour l'évaluation des projets CPI25.

Objectifs:
  - Lire la composition des groupes depuis groupes.ods (sans dépendance externe).
  - Calculer la note finale /20 avec la formule CORRIGEE (cf. REVUE_EVALUATION.md).
  - Générer un squelette eval.md par groupe, prêt à remplir.
  - Fournir un self-test garantissant la reproductibilité du calcul.

Le calcul de note est centralisé ici : le correcteur (humain ou LLM) se contente
de renseigner les 19 notes (0 à 4). Aucune arithmétique n'est laissée au LLM, ce
qui rend la note déterministe et reproductible.

Commandes:
  roster     Afficher la composition des groupes (lue depuis groupes.ods).
  note       Calculer une note à partir de 19 valeurs (0..4) séparées par des virgules.
  skeleton   Générer/écraser G*/eval.md (squelette) pour chaque groupe du roster.
  selftest   Vérifier le calcul de note sur des cas connus.

Dépendances: bibliothèque standard uniquement (Python 3.8+).
"""
import argparse
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ODS_PATH = os.path.join(ROOT, "groupes.ods")

# Espaces de noms OpenDocument
NS = {
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}

VALID_NOTES = {0, 1, 2, 3, 4}

# Intitulés des 19 critères (alignés sur evaluation.md).
CRITERIA = [
    (1, "Analyse des recommandations ANSSI (Sécurité)", "principal"),
    (2, "Procédure d'installation et configuration serveur", "principal"),
    (3, "Documentation utilisateur", "principal"),
    (4, "Tests de validation basés sur les use cases", "principal"),
    (5, "Contexte initial du projet", "principal"),
    (6, "Besoins exprimés (expression du besoin / évolutions)", "principal"),
    (7, "Objectifs du projet", "principal"),
    (8, "Fonctions principales", "principal"),
    (9, "Tâches détaillées par livrables et par personnes", "principal"),
    (10, "UML Use Case (conformité aux normes UML)", "principal"),
    (11, "UML Diagramme de blocs ou de déploiement", "principal"),
    (12, "Schéma synoptique / réseau du projet", "principal"),
    (13, "Diagramme sitemap des différentes pages", "principal"),
    (14, "Mockup partiel du projet", "principal"),
    (15, "Code PHP - Architecture logicielle MVC", "principal"),
    (16, "Programmation modulaire (fichiers source/fonctions)", "principal"),
    (17, "Programmation orientée objet (BONUS)", "bonus"),
    (18, "Utilisation PHPStan (BONUS)", "bonus"),
    (19, "Tests unitaires (BONUS)", "bonus"),
]

MAIN_IDS = [n for n, _, kind in CRITERIA if kind == "principal"]   # 1..16
BONUS_IDS = [n for n, _, kind in CRITERIA if kind == "bonus"]      # 17..19
NOTE_MAX = 4  # note maximale par critère


# --------------------------------------------------------------------------- #
# Lecture du fichier groupes.ods
# --------------------------------------------------------------------------- #
def _cell_text(cell):
    """Concatène le texte des paragraphes d'une cellule ODS."""
    parts = []
    for p in cell.iter("{%s}p" % NS["text"]):
        parts.append("".join(p.itertext()))
    return " ".join(t for t in parts if t).strip()


def parse_roster(ods_path=ODS_PATH):
    """Retourne une liste ordonnée de tuples (groupe, [membres]).

    Format attendu de la feuille: colonnes [Groupe, Nom, Prénom, repository].
    Le libellé de groupe (G1, G2, ...) n'apparaît que sur la 1re ligne d'un
    groupe ; les lignes suivantes (colonne Groupe vide) appartiennent au même
    groupe.
    """
    with zipfile.ZipFile(ods_path) as z:
        xml = z.read("content.xml")
    root = ET.fromstring(xml)

    groups = []          # [(group_label, [member, ...])]
    index = {}           # group_label -> position dans groups
    current = None

    for table in root.iter("{%s}table" % NS["table"]):
        for row in table.iter("{%s}table-row" % NS["table"]):
            cells = []
            for cell in row.findall("{%s}table-cell" % NS["table"]):
                rep = int(cell.get("{%s}number-columns-repeated" % NS["table"], "1"))
                rep = rep if rep <= 8 else 1  # ignore les répétitions de remplissage
                txt = _cell_text(cell)
                cells.extend([txt] * rep)
            while len(cells) < 3:
                cells.append("")

            grp, nom, prenom = cells[0].strip(), cells[1].strip(), cells[2].strip()

            # Ligne d'en-tête éventuelle
            if not grp and not nom and not prenom:
                continue
            if "repository" in (cells[3].lower() if len(cells) > 3 else "") and not nom:
                continue

            if grp:
                current = grp
                if current not in index:
                    index[current] = len(groups)
                    groups.append((current, []))
            if current is None:
                continue
            if nom or prenom:
                member = " ".join(x for x in (nom, prenom) if x)
                groups[index[current]][1].append(member)

    return groups


# --------------------------------------------------------------------------- #
# Calcul de note (formule corrigée)
# --------------------------------------------------------------------------- #
def round_half_nearest(x):
    """Arrondi au 0,5 le plus proche (spécification documentée du projet)."""
    return round(x * 2) / 2.0


def compute_note(scores):
    """Calcule la note finale /20.

    `scores` : dict {numero_critere(1..19) -> note(0..4)}. Les critères absents
    valent 0.

    Formule (corrigée) :
        principal = (Σ critères 1..16) / (16 * 4) * 20 * 0,9   -> max 18
        bonus     = (Σ critères 17..19) / (3 * 4)  * 20 * 0,1   -> max 2
        note      = principal + bonus                           -> max 20
    """
    main_sum = sum(float(scores.get(i, 0)) for i in MAIN_IDS)
    bonus_sum = sum(float(scores.get(i, 0)) for i in BONUS_IDS)

    main_part = main_sum / (len(MAIN_IDS) * NOTE_MAX) * 20 * 0.9
    bonus_part = bonus_sum / (len(BONUS_IDS) * NOTE_MAX) * 20 * 0.1
    raw = main_part + bonus_part

    return {
        "main_sum": main_sum,
        "bonus_sum": bonus_sum,
        "main_part": main_part,
        "bonus_part": bonus_part,
        "raw": raw,
        "rounded": round_half_nearest(raw),
    }


def parse_scores_arg(arg):
    """'4,4,3,...' (19 valeurs) -> dict {1:.., 2:.., ...}."""
    vals = [v.strip().replace(",", ".") for v in arg.split(";")] if ";" in arg else \
           [v.strip() for v in arg.split(",")]
    if len(vals) != len(CRITERIA):
        raise ValueError("Il faut exactement %d valeurs (reçu %d)."
                         % (len(CRITERIA), len(vals)))
    scores = {}
    for (num, _, _), raw in zip(CRITERIA, vals):
        f = float(raw)
        if f not in VALID_NOTES:
            raise ValueError("Note invalide '%s' pour le critère %d (attendu 0..4)."
                             % (raw, num))
        scores[num] = f
    return scores


# --------------------------------------------------------------------------- #
# Génération du squelette eval.md
# --------------------------------------------------------------------------- #
def render_skeleton(group_label, members, deliverable_present=False):
    today = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append("# Évaluation Groupe %s" % group_label)
    lines.append("")
    lines.append("- **Date de génération** : %s" % today)
    lines.append("- **Membres du groupe** :")
    for m in members:
        lines.append("  - %s" % m)
    if not members:
        lines.append("  - (non renseigné)")
    lines.append("- **Dépôt évalué** : _à renseigner_")
    lines.append("- **Grille** : evaluation.md (19 critères, note /4 par critère)")
    lines.append("- **Calcul** : centralisé par `tools/cpi_eval.py` (formule corrigée)")
    lines.append("")

    if not deliverable_present:
        lines.append("> ⚠️ **Aucun rendu présent dans `%s/` à la date de génération.**" % group_label)
        lines.append("> Ce fichier est un *squelette* prêt à remplir dès réception du dépôt étudiant.")
        lines.append("> Renseigner chaque note (0 à 4) puis recalculer avec :")
        lines.append(">")
        lines.append("> ```bash")
        lines.append("> python3 tools/cpi_eval.py note --scores \"4,4,3,...\"  # 19 valeurs")
        lines.append("> ```")
        lines.append("")

    lines.append("## Barème de notation (rappel)")
    lines.append("")
    lines.append("| Note | Signification |")
    lines.append("|:---:|---|")
    lines.append("| 0 | Non réalisé, inexistant |")
    lines.append("| 1 | Abordé superficiellement, incomplet |")
    lines.append("| 2 | Partiellement réalisé |")
    lines.append("| 3 | Bien réalisé, erreurs mineures |")
    lines.append("| 4 | Très bien réalisé, complet, conforme |")
    lines.append("")

    lines.append("## Critères principaux (90 % — max 18/20)")
    lines.append("")
    for num, title, kind in CRITERIA:
        if kind != "principal":
            continue
        lines.append("### %d. %s : _[0-4]_" % (num, title))
        lines.append("")
        lines.append("- **Preuve / fichier(s)** : _chemin ou lien justifiant la note_")
        lines.append("- **Justification** : _à compléter_")
        lines.append("")

    lines.append("## Critères bonus (10 % — max 2/20)")
    lines.append("")
    for num, title, kind in CRITERIA:
        if kind != "bonus":
            continue
        lines.append("### %d. %s : _[0-4]_" % (num, title))
        lines.append("")
        lines.append("- **Preuve / fichier(s)** : _chemin ou lien justifiant la note_")
        lines.append("- **Justification** : _à compléter_")
        lines.append("")

    lines.append("## Tableau de saisie (à remplir)")
    lines.append("")
    lines.append("| # | Critère | Note (0-4) |")
    lines.append("|:---:|---|:---:|")
    for num, title, _ in CRITERIA:
        lines.append("| %d | %s | |" % (num, title))
    lines.append("")

    lines.append("## Note finale proposée : _[X]/20_")
    lines.append("")
    lines.append("**Formule (corrigée)** :")
    lines.append("")
    lines.append("```")
    lines.append("note = (Σ critères 1-16)/(16×4) × 20 × 0,9   (max 18)")
    lines.append("     + (Σ critères 17-19)/(3×4) × 20 × 0,1   (max 2)")
    lines.append("```")
    lines.append("")
    lines.append("_Calcul reproductible :_ `python3 tools/cpi_eval.py note --scores \"...\"`")
    lines.append("")

    lines.append("## Points forts")
    lines.append("")
    lines.append("- _à compléter_")
    lines.append("")
    lines.append("## Points d'amélioration")
    lines.append("")
    lines.append("- _à compléter_")
    lines.append("")
    lines.append("---")
    lines.append("_Squelette généré par `tools/cpi_eval.py`._")
    lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Commandes CLI
# --------------------------------------------------------------------------- #
def cmd_roster(args):
    groups = parse_roster(args.ods)
    for label, members in groups:
        print("%s (%d membre%s):" % (label, len(members), "s" if len(members) > 1 else ""))
        for m in members:
            print("  - %s" % m)
    return 0


def cmd_note(args):
    scores = parse_scores_arg(args.scores)
    r = compute_note(scores)
    print("Σ principaux (1-16) : %.2f / %d" % (r["main_sum"], len(MAIN_IDS) * NOTE_MAX))
    print("Σ bonus     (17-19) : %.2f / %d" % (r["bonus_sum"], len(BONUS_IDS) * NOTE_MAX))
    print("Part principale (90%%) : %.3f / 18" % r["main_part"])
    print("Part bonus      (10%%) : %.3f / 2" % r["bonus_part"])
    print("Note brute          : %.3f / 20" % r["raw"])
    print("Note arrondie (0,5) : %.1f / 20" % r["rounded"])
    return 0


def cmd_skeleton(args):
    groups = parse_roster(args.ods)
    written = 0
    for label, members in groups:
        group_dir = os.path.join(args.out_root, label)
        if not os.path.isdir(group_dir):
            if args.create_dirs:
                os.makedirs(group_dir, exist_ok=True)
            else:
                print("  ! dossier absent, ignoré: %s" % group_dir, file=sys.stderr)
                continue
        # Un rendu est "présent" si le dossier contient autre chose que eval.md
        existing = [f for f in os.listdir(group_dir) if f != "eval.md"]
        present = len(existing) > 0
        path = os.path.join(group_dir, "eval.md")
        if os.path.exists(path) and not args.force:
            print("  = existe déjà (utiliser --force pour écraser): %s" % path)
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_skeleton(label, members, deliverable_present=present))
        written += 1
        print("  + écrit: %s%s" % (path, "  [rendu détecté]" if present else "  [squelette vide]"))
    print("%d fichier(s) eval.md généré(s)." % written)
    return 0


def cmd_selftest(args):
    cases = [
        ("Tout parfait (19 × 4)", {i: 4 for i in range(1, 20)}, 20.0),
        ("Principaux parfaits, bonus nuls", {i: 4 for i in MAIN_IDS}, 18.0),
        ("Bonus parfaits, principaux nuls", {i: 4 for i in BONUS_IDS}, 2.0),
        ("Tout à zéro", {}, 0.0),
        ("Tout à 2 (moitié)", {i: 2 for i in range(1, 20)}, 10.0),
    ]
    ok = True
    for label, scores, expected in cases:
        r = compute_note(scores)
        status = "OK " if abs(r["raw"] - expected) < 1e-9 else "ECHEC"
        if status != "OK ":
            ok = False
        print("[%s] %-35s brut=%.3f attendu=%.3f arrondi=%.1f"
              % (status, label, r["raw"], expected, r["rounded"]))
    print("\nRésultat: %s" % ("tous les cas passent." if ok else "des cas ECHOUENT."))
    return 0 if ok else 1


def build_parser():
    p = argparse.ArgumentParser(prog="cpi_eval", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("roster", help="Afficher la composition des groupes")
    sp.add_argument("--ods", default=ODS_PATH)
    sp.set_defaults(func=cmd_roster)

    sp = sub.add_parser("note", help="Calculer une note à partir de 19 valeurs (0..4)")
    sp.add_argument("--scores", required=True,
                    help="19 valeurs 0..4 séparées par des virgules (ou ';')")
    sp.set_defaults(func=cmd_note)

    sp = sub.add_parser("skeleton", help="Générer G*/eval.md (squelette)")
    sp.add_argument("--ods", default=ODS_PATH)
    sp.add_argument("--out-root", default=ROOT)
    sp.add_argument("--force", action="store_true", help="Écraser un eval.md existant")
    sp.add_argument("--create-dirs", action="store_true",
                    help="Créer le dossier de groupe s'il n'existe pas")
    sp.set_defaults(func=cmd_skeleton)

    sp = sub.add_parser("selftest", help="Vérifier le calcul de note")
    sp.set_defaults(func=cmd_selftest)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
