#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcul des notes d'évaluation, piloté par fichiers (ré-exécutable).

Sources (par groupe, dans eval/G*/):
  - input.json      : étudiants + participation (%), fourni par les étudiants
  - evaluation.md   : niveaux (0 / 0,25 / 0,5 / 0,75 / 1) saisis par le correcteur
                      dans les tableaux « ## Détail — … » (colonne Niveau)
Grille:
  - eval/bareme.json : parties, critères, coefficients, pondérations

eval.py lit ces fichiers, calcule la note de groupe et les notes individuelles,
puis (commande `write`) réécrit le bloc calculé délimité par les marqueurs
<!-- eval:calcul début … --> … <!-- eval:calcul fin --> dans chaque evaluation.md.
L'opération est idempotente : on peut la relancer autant de fois que voulu.

Commandes:
  compute            Afficher les notes calculées (aperçu, sans écrire).
  write              Réécrire le bloc calculé dans chaque eval/G*/evaluation.md.
  commits --repo P   Compte-rendu des commits Git par auteur (traçabilité).
"""
import argparse
import glob
import json
import os
import re
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # …/eval
BAREME_PATH = os.path.join(BASE_DIR, "bareme.json")
OUT_DIR = os.path.join(BASE_DIR, "out")
GROUPS_GLOB = os.path.join(BASE_DIR, "G*")

VALID_VALUES = {0, 0.25, 0.5, 0.75, 1}

MARK_BEGIN = ("<!-- eval:calcul début — généré par eval.py "
              "(python3 eval/eval.py write) ; ne pas éditer à la main -->")
MARK_END = "<!-- eval:calcul fin -->"


# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #
def round_half_nearest(x: float) -> float:
    """Arrondi au 0,5 le plus proche. 14,1 -> 14,0 ; 14,3 -> 14,5."""
    return int(x * 2 + 0.5) / 2.0

def fr(x: float, dec: int = 2) -> str:
    """Formatage français (virgule décimale)."""
    return f"{x:.{dec}f}".replace(".", ",")

def load_bareme():
    with open(BAREME_PATH, encoding="utf-8") as f:
        return json.load(f)

def group_dirs():
    return sorted(d for d in glob.glob(GROUPS_GLOB) if os.path.isdir(d))


# --------------------------------------------------------------------------- #
# Lecture des sources
# --------------------------------------------------------------------------- #
def load_input(group_dir):
    """input.json -> dict ; {} si absent."""
    path = os.path.join(group_dir, "input.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def parse_niveaux(eval_md_path):
    """Extrait {numero_critère(1..24) -> niveau(float)} des tableaux Détail.

    Lit les lignes « | <n> | <critère> | <niveau> | <commentaire> | » où la
    1re cellule est un entier 1..24 ; cellule vide -> critère non noté (absent
    du dict). Lève ValueError sur un niveau hors barème.
    """
    niveaux = {}
    if not os.path.isfile(eval_md_path):
        return niveaux
    with open(eval_md_path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s.startswith("|"):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 3 or not cells[0].isdigit():
                continue
            num = int(cells[0])
            if not (1 <= num <= 24):
                continue
            raw = cells[2].replace(",", ".").strip()
            if raw == "":
                continue
            val = float(raw)
            if val not in VALID_VALUES:
                raise ValueError(
                    f"{eval_md_path}: niveau invalide '{cells[2]}' pour le "
                    f"critère {num} (attendu 0 / 0,25 / 0,5 / 0,75 / 1).")
            niveaux[num] = val
    return niveaux


# --------------------------------------------------------------------------- #
# Calcul
# --------------------------------------------------------------------------- #
def compute_group(bareme, niveaux):
    """Retourne (note_arrondie, note_brute, [(nom_partie, score, points_max, poids_pct)])."""
    part_scores = []
    total_score = 0.0
    total_max = 0.0
    for partie in bareme["parties"]:
        crit = partie["criteres"]
        coeff_sum = sum(c.get("coefficient", 1) for c in crit)
        weighted = sum(niveaux.get(c["id"], 0.0) * c.get("coefficient", 1) for c in crit)
        ratio = (weighted / coeff_sum) if coeff_sum else 0.0
        score = partie["points_max"] * ratio
        total_score += score
        total_max += partie["points_max"]
        part_scores.append((partie["nom"], score, partie["points_max"], partie.get("poids_pct")))
    note_brut = (total_score / total_max) * 20 if total_max else 0.0
    return round_half_nearest(note_brut), note_brut, part_scores

def individual_rows(group_note, students):
    """Retourne [(nom, participation, note_individuelle)] pour le bloc calculé."""
    n = len(students)
    if n == 0:
        return []
    equal = 100.0 / n
    rows = []
    for s in students:
        name = f"{s.get('nom', '')} {s.get('prenom', '')}".strip()
        part = s.get("participation_pct")
        if part is None:
            indiv = group_note
            rows.append((name, None, indiv))
        else:
            factor = (part / equal) if equal else 1.0
            indiv = min(20.0, round_half_nearest(group_note * factor))
            rows.append((name, part, indiv))
    return rows

def count_ungraded(bareme, niveaux):
    ids = [c["id"] for p in bareme["parties"] for c in p["criteres"]]
    return sum(1 for i in ids if i not in niveaux)


# --------------------------------------------------------------------------- #
# Rendu / écriture du bloc calculé
# --------------------------------------------------------------------------- #
def render_block(note, note_brut, part_scores, indiv_rows):
    L = [MARK_BEGIN, ""]
    L.append(f"## Note de groupe : **{fr(note, 1)} / 20** _(brut {fr(note_brut, 2)})_")
    L.append("")
    L.append("| Partie | Score | Poids |")
    L.append("|---|:--:|:--:|")
    for nom, score, pmax, poids in part_scores:
        poids_str = f"{poids} %" if poids is not None else ""
        L.append(f"| {nom} | {fr(score, 2)} / {fr(pmax, 0)} | {poids_str} |")
    L.append("")
    L.append("### Notes individuelles (participation)")
    L.append("")
    L.append("| Étudiant | Participation | Note individuelle |")
    L.append("|---|:--:|:--:|")
    if indiv_rows:
        for name, part, indiv in indiv_rows:
            part_str = f"{fr(part, 0)} %" if part is not None else "—"
            L.append(f"| {name} | {part_str} | {fr(indiv, 1)} / 20 |")
    else:
        L.append("| _(aucun étudiant dans input.json)_ | | |")
    L.append("")
    L.append(MARK_END)
    return "\n".join(L)

def write_block(eval_md_path, block):
    """Insère ou remplace le bloc calculé entre les marqueurs (idempotent)."""
    with open(eval_md_path, encoding="utf-8") as f:
        content = f.read()

    if MARK_BEGIN in content and MARK_END in content:
        pre = content[:content.index(MARK_BEGIN)]
        post = content[content.index(MARK_END) + len(MARK_END):]
        new = pre + block + post
    else:
        # Pas de marqueurs : insérer après le titre H1.
        lines = content.splitlines(keepends=True)
        out, inserted = [], False
        for ln in lines:
            out.append(ln)
            if not inserted and ln.lstrip().startswith("# "):
                out.append("\n" + block + "\n")
                inserted = True
        if not inserted:
            out.insert(0, block + "\n\n")
        new = "".join(out)

    with open(eval_md_path, "w", encoding="utf-8") as f:
        f.write(new)


# --------------------------------------------------------------------------- #
# Commandes
# --------------------------------------------------------------------------- #
def iter_groups(bareme):
    """Génère (label, group_dir, data, niveaux, note, note_brut, part_scores, indiv_rows, ungraded)."""
    for group_dir in group_dirs():
        label = os.path.basename(group_dir)
        data = load_input(group_dir)
        eval_md = os.path.join(group_dir, "evaluation.md")
        niveaux = parse_niveaux(eval_md)
        note, note_brut, part_scores = compute_group(bareme, niveaux)
        indiv = individual_rows(note, data.get("etudiants", []))
        ungraded = count_ungraded(bareme, niveaux)
        yield label, group_dir, data, niveaux, note, note_brut, part_scores, indiv, ungraded

def cmd_compute(args):
    bareme = load_bareme()
    for (label, _gd, _data, _niv, note, note_brut, part_scores, indiv,
         ungraded) in iter_groups(bareme):
        print(f"\n{label} : {fr(note, 1)}/20 (brut {fr(note_brut, 2)})"
              + (f"  ⚠️ {ungraded} critère(s) non noté(s)" if ungraded else ""))
        for nom, score, pmax, _poids in part_scores:
            print(f"  - {nom} : {fr(score, 2)} / {fr(pmax, 0)}")
        for name, part, ind in indiv:
            part_str = f"{fr(part, 0)}%" if part is not None else "—"
            print(f"    · {name} : {fr(ind, 1)}/20 (participation {part_str})")
    return 0

def cmd_write(args):
    bareme = load_bareme()
    written = 0
    for (label, group_dir, _data, _niv, note, note_brut, part_scores, indiv,
         ungraded) in iter_groups(bareme):
        eval_md = os.path.join(group_dir, "evaluation.md")
        if not os.path.isfile(eval_md):
            print(f"  ! {label} : evaluation.md absent, ignoré.")
            continue
        block = render_block(note, note_brut, part_scores, indiv)
        write_block(eval_md, block)
        written += 1
        warn = f"  ⚠️ {ungraded} critère(s) non noté(s)" if ungraded else ""
        print(f"  + {label} : {fr(note, 1)}/20 écrit dans evaluation.md{warn}")
    print(f"{written} fichier(s) evaluation.md mis à jour.")
    return 0

def sanitize_filename(name: str) -> str:
    bad = '<>:"/\\|?*'
    return "".join(c if c not in bad else "_" for c in name).replace(" ", "_")

def cmd_commits(args):
    repo = args.repo
    inside = subprocess.run(["git", "-C", repo, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        print(f"Pas un dépôt Git valide : {repo}")
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    sl = subprocess.run(["git", "-C", repo, "shortlog", "-sne", "--all", "--no-merges"],
                        capture_output=True, text=True).stdout.strip().splitlines()

    repo_label = os.path.basename(os.path.abspath(repo))
    lines = [f"# Compte-rendu des commits - {repo_label}", ""]
    lines.append(f"- Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- Dépôt : `{repo}`")
    lines.append("")

    authors = []
    for l in sl:
        count_str, author = l.strip().split("\t", 1)
        authors.append((int(count_str), author))
    total = sum(c for c, _ in authors)

    lines.append(f"**Total commits (hors merges)** : {total}")
    lines.append("")
    lines.append("| Commits | Part | Auteur |")
    lines.append("|---:|---:|---|")
    for count, author in authors:
        part = (100.0 * count / total) if total else 0.0
        lines.append(f"| {count} | {part:.0f}% | {author} |")
    lines.append("")

    for count, author in authors:
        m = re.match(r"^(.*) <(.*)>$", author)
        name = m.group(1) if m else author
        log = subprocess.run(
            ["git", "-C", repo, "log", "--all", "--no-merges", f"--author={name}",
             "--pretty=format:- %ad %h %s", "--date=short"],
            capture_output=True, text=True).stdout.strip()
        lines.append(f"## {author} — {count} commit(s)")
        lines.append("")
        lines.append(log if log else "_(aucun)_")
        lines.append("")

    out = os.path.join(OUT_DIR, f"commits_{sanitize_filename(repo_label)}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Compte-rendu écrit dans {out} ({total} commits, {len(authors)} auteur(s)).")
    return 0

def build_parser():
    p = argparse.ArgumentParser(prog="eval", description="Calcul des notes (piloté par fichiers)")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("compute", help="Afficher les notes calculées (aperçu)")
    sp.set_defaults(func=cmd_compute)

    sp = sub.add_parser("write", help="Réécrire le bloc calculé dans chaque evaluation.md")
    sp.set_defaults(func=cmd_write)

    sp = sub.add_parser("commits", help="Compte-rendu des commits Git par auteur")
    sp.add_argument("--repo", required=True, help="Chemin du dépôt Git de l'étudiant/groupe")
    sp.set_defaults(func=cmd_commits)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    raise SystemExit(args.func(args))

if __name__ == "__main__":
    main()
