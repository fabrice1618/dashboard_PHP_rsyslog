#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application CLI pour gérer des évaluations et générer des rapports Markdown.
Base SQLite: eval/evaluation.db

Commandes:
  - seed        : créer une évaluation pré-remplie avec la grille (evaluation.md)
  - config      : créer une évaluation, parties, questions (manuel)
  - load        : charger des étudiants depuis un fichier texte (groupe;nom)
  - charge      : saisir la charge déclarative (%) de chaque étudiant (C9)
  - grade       : saisir les notes (par étudiant)
  - list        : lister les étudiants et l'état de complétude
  - compute     : calculer les notes finales (aperçu)
  - commits     : compte-rendu des commits Git par auteur (traçabilité)
  - export      : générer les fichiers Markdown (un par étudiant)
  - validate    : valider l'évaluation (puis export)
"""
import argparse
import os
import re
import sqlite3
import subprocess
from datetime import datetime

DB_DIR = os.path.join("eval")
DB_PATH = os.path.join(DB_DIR, "evaluation.db")
OUT_DIR = os.path.join("eval", "out")

VALID_VALUES = {0, 0.25, 0.5, 0.75, 1}

# Grille canonique alignée sur evaluation.md.
# Deux parties pondérées : principal /18 (90 %) + qualité logicielle avancée /2 (10 %).
# Chaque critère est créé avec un coefficient 1 par défaut (modifiable via 'config').
GRILLE = [
    ("Critères principaux", 18.0, [
        "1. Analyse des recommandations ANSSI",
        "2. Procédure d'installation et configuration serveur",
        "3. Documentation utilisateur",
        "4. Tests de validation (use cases)",
        "5. Contexte initial du projet",
        "6. Besoins exprimés (expression du besoin / évolutions)",
        "7. Objectifs du projet",
        "8. Fonctions principales",
        "9. Tâches détaillées par livrables et par personnes",
        "10. UML Use Case",
        "11. UML diagramme de blocs ou de déploiement",
        "12. Schéma synoptique du projet",
        "13. Sitemap des pages",
        "14. Mockup partiel du projet",
        "15. Code PHP — Architecture MVC",
        "16. Programmation modulaire",
        "17. Critères de performances",
        "18. Contraintes techniques",
        "19. Matériels et logiciels mis en œuvre",
        "20. Traçabilité des commits par étudiant",
        "21. Échanges avec les IA (prompt / résultat)",
    ]),
    ("Qualité logicielle avancée (10 %)", 2.0, [
        "22. Programmation orientée objet",
        "23. Utilisation de PHPStan",
        "24. Tests unitaires",
    ]),
]

def ensure_dirs():
    os.makedirs(DB_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

def get_conn():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS evaluation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft' -- 'draft' | 'validated'
    );

    CREATE TABLE IF NOT EXISTS part (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluation_id INTEGER NOT NULL REFERENCES evaluation(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        max_points REAL NOT NULL CHECK (max_points > 0),
        ord INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER NOT NULL REFERENCES part(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        coefficient REAL NOT NULL CHECK (coefficient > 0),
        ord INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluation_id INTEGER NOT NULL REFERENCES evaluation(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        group_name TEXT,     -- groupe d'appartenance (pour l'individualisation C9)
        charge REAL          -- charge déclarative en % (modulation individuelle C9)
    );

    -- note.value in {0,0.25,0.5,0.75,1}
    CREATE TABLE IF NOT EXISTS note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL REFERENCES student(id) ON DELETE CASCADE,
        question_id INTEGER NOT NULL REFERENCES question(id) ON DELETE CASCADE,
        value REAL NOT NULL,
        comment TEXT,
        UNIQUE(student_id, question_id)
    );
    """)
    conn.commit()
    migrate(conn)

def migrate(conn):
    # Ajoute les colonnes group_name / charge aux bases créées avant l'individualisation (C9).
    cur = conn.cursor()
    cols = [r["name"] for r in cur.execute("PRAGMA table_info(student)")]
    if "group_name" not in cols:
        cur.execute("ALTER TABLE student ADD COLUMN group_name TEXT")
    if "charge" not in cols:
        cur.execute("ALTER TABLE student ADD COLUMN charge REAL")
    conn.commit()

def latest_eval_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM evaluation ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    return row["id"] if row else None

def round_half_nearest(x: float) -> float:
    # Arrondi au 0,5 le plus proche (cf. revue C5). 14,1 -> 14,0 ; 14,3 -> 14,5.
    return int(x * 2 + 0.5) / 2.0

def cmd_config(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()

    title = input("Titre de l'évaluation: ").strip()
    if not title:
        print("Titre requis.")
        return
    cur.execute("INSERT INTO evaluation(title, created_at, status) VALUES (?, ?, 'draft')",
                (title, datetime.now().isoformat(timespec="seconds")))
    eval_id = cur.lastrowid

    print("\nDéfinissez les parties. Entrez 0 pour terminer.")
    part_index = 1
    while True:
        name = input(f"Nom de la partie {part_index} (ou 0 pour terminer): ").strip()
        if name == "0":
            break
        if not name:
            print("Nom requis.")
            continue
        try:
            max_points = float(input(f"Points max pour '{name}': ").replace(",", "."))
            if max_points <= 0:
                raise ValueError
        except Exception:
            print("Veuillez entrer un nombre de points > 0.")
            continue

        cur.execute("INSERT INTO part(evaluation_id, name, max_points, ord) VALUES (?, ?, ?, ?)",
                    (eval_id, name, max_points, part_index))
        part_id = cur.lastrowid

        print(f"Ajoutez des questions pour la partie '{name}'. Entrez 0 pour terminer.")
        q_index = 1
        while True:
            qname = input(f"  - Nom de la question {q_index} (ou 0 pour terminer): ").strip()
            if qname == "0":
                break
            if not qname:
                print("  Nom requis.")
                continue
            raw_coeff = input(f"    Coefficient pour '{qname}' [1]: ").strip().replace(",", ".")
            if raw_coeff == "":
                coeff = 1.0
            else:
                try:
                    coeff = float(raw_coeff)
                    if coeff <= 0:
                        raise ValueError
                except Exception:
                    print("    Coefficient > 0 requis.")
                    continue
            cur.execute("INSERT INTO question(part_id, name, coefficient, ord) VALUES (?, ?, ?, ?)",
                        (part_id, qname, coeff, q_index))
            q_index += 1

        part_index += 1

    conn.commit()
    print(f"\nÉvaluation créée (id={eval_id}). Utilisez 'eval load' pour charger les étudiants.")

def cmd_seed(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()

    title = (args.title or "Projet dashboard PHP/rsyslog").strip()
    cur.execute("INSERT INTO evaluation(title, created_at, status) VALUES (?, ?, 'draft')",
                (title, datetime.now().isoformat(timespec="seconds")))
    eval_id = cur.lastrowid

    part_ord = 1
    n_q = 0
    for part_name, max_points, questions in GRILLE:
        cur.execute("INSERT INTO part(evaluation_id, name, max_points, ord) VALUES (?, ?, ?, ?)",
                    (eval_id, part_name, max_points, part_ord))
        part_id = cur.lastrowid
        for q_ord, qname in enumerate(questions, start=1):
            cur.execute("INSERT INTO question(part_id, name, coefficient, ord) VALUES (?, ?, ?, ?)",
                        (part_id, qname, 1.0, q_ord))
            n_q += 1
        part_ord += 1

    conn.commit()
    print(f"Évaluation '{title}' créée (id={eval_id}) avec la grille canonique "
          f"({n_q} critères, coef 1, parties /18 + /2).")
    print("Suite : 'eval load <fichier>' (groupe;nom), 'eval charge', puis 'eval grade'.")

def cmd_load(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation. Lancez d'abord 'eval config'.")
        return

    path = args.file
    if not os.path.isfile(path):
        print(f"Fichier introuvable: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        rows = [line.strip() for line in f if line.strip()]
    if not rows:
        print("Aucun nom d'étudiant dans le fichier.")
        return

    inserted = 0
    for row in rows:
        # Format accepté : "Groupe;Nom", "Groupe<TAB>Nom" ou simplement "Nom".
        parts = re.split(r"[;\t]", row, maxsplit=1)
        if len(parts) == 2:
            group_name, name = parts[0].strip(), parts[1].strip()
        else:
            group_name, name = None, parts[0].strip()
        if not name:
            continue
        cur.execute("INSERT INTO student(evaluation_id, name, group_name) VALUES (?, ?, ?)",
                    (eval_id, name, group_name))
        inserted += 1
    conn.commit()
    print(f"{inserted} étudiants importés pour l'évaluation {eval_id}.")

def cmd_charge(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return
    students = list_students(conn, eval_id)
    if not students:
        print("Aucun étudiant. Utilisez 'eval load'.")
        return
    print("Charge déclarative (%) par étudiant. Entrée vide = inchangé.\n")
    for s in students:
        grp = s["group_name"] or "—"
        shown = f"{s['charge']:g}%" if s["charge"] is not None else "non renseignée"
        raw = input(f"- [{grp}] {s['name']} (actuel: {shown}) : ").strip().replace(",", ".").rstrip("%")
        if raw == "":
            continue
        try:
            val = float(raw)
            if val < 0:
                raise ValueError
        except Exception:
            print("  Valeur invalide, ignorée.")
            continue
        cur.execute("UPDATE student SET charge=? WHERE id=?", (val, s["id"]))
        conn.commit()
    # Contrôle : la somme des charges d'un groupe devrait valoir 100 %.
    cur.execute("""SELECT group_name, SUM(charge) AS tot FROM student
                   WHERE evaluation_id=? AND group_name IS NOT NULL AND charge IS NOT NULL
                   GROUP BY group_name""", (eval_id,))
    for r in cur.fetchall():
        if r["tot"] is not None and abs(r["tot"] - 100.0) > 0.01:
            print(f"  ⚠️ Groupe {r['group_name']} : somme des charges = {r['tot']:g}% (attendu 100%).")
    print("Charges enregistrées.")

def fetch_structure(conn, eval_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM part WHERE evaluation_id=? ORDER BY ord ASC", (eval_id,))
    parts = cur.fetchall()
    part_ids = [p["id"] for p in parts]
    qs_by_part = {}
    for pid in part_ids:
        cur.execute("SELECT * FROM question WHERE part_id=? ORDER BY ord ASC", (pid,))
        qs_by_part[pid] = cur.fetchall()
    return parts, qs_by_part

def list_students(conn, eval_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE evaluation_id=? ORDER BY id ASC", (eval_id,))
    return cur.fetchall()

def student_progress(conn, student_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(q.id) AS total_q
        FROM question q
        JOIN part p ON p.id = q.part_id
        JOIN student s ON s.evaluation_id = p.evaluation_id
        WHERE s.id = ?
    """, (student_id,))
    total_q = cur.fetchone()["total_q"]

    cur.execute("SELECT COUNT(*) AS c FROM note WHERE student_id=?", (student_id,))
    done = cur.fetchone()["c"]
    return done, total_q

def cmd_list(args):
    conn = get_conn()
    init_db(conn)
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return
    students = list_students(conn, eval_id)
    print(f"Étudiants de l'évaluation {eval_id}:")
    for s in students:
        done, total = student_progress(conn, s["id"])
        status = "complet" if done == total and total > 0 else f"{done}/{total}"
        print(f"- [{status}] {s['name']} (id={s['id']})")

def prompt_value():
    while True:
        raw = input("    Évaluation (0, 0.25, 0.5, 0.75, 1): ").strip().replace(",", ".")
        try:
            val = float(raw)
            if val in VALID_VALUES:
                return val
        except Exception:
            pass
        print("    Valeur invalide. Choisir parmi 0, 0.25, 0.5, 0.75, 1.")

def cmd_grade(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return

    # choisir l'étudiant
    if args.student_id:
        cur.execute("SELECT * FROM student WHERE id=? AND evaluation_id=?", (args.student_id, eval_id))
        student = cur.fetchone()
        if not student:
            print(f"Étudiant id={args.student_id} introuvable.")
            return
    elif args.student_name:
        cur.execute("SELECT * FROM student WHERE name=? AND evaluation_id=?", (args.student_name, eval_id))
        student = cur.fetchone()
        if not student:
            print(f"Étudiant '{args.student_name}' introuvable.")
            return
    else:
        studs = list_students(conn, eval_id)
        if not studs:
            print("Aucun étudiant. Utilisez 'eval load'.")
            return
        print("Choisissez un étudiant par id:")
        for s in studs:
            done, total = student_progress(conn, s["id"])
            print(f"- id={s['id']} | {s['name']} [{done}/{total}]")
        try:
            sid = int(input("id: "))
        except Exception:
            print("Entrée invalide.")
            return
        cur.execute("SELECT * FROM student WHERE id=? AND evaluation_id=?", (sid, eval_id))
        student = cur.fetchone()
        if not student:
            print("id invalide.")
            return

    parts, qs_by_part = fetch_structure(conn, eval_id)
    if not parts:
        print("Évaluation sans parties/questions. Lancez 'eval config'.")
        return

    print(f"\nSaisie pour: {student['name']} (id={student['id']})\n")
    for p in parts:
        print(f"Partie: {p['name']} (/{p['max_points']})")
        qs = qs_by_part[p["id"]]
        # récupérer notes existantes
        for q in qs:
            # afficher existant s'il y en a
            cur.execute("SELECT value, comment FROM note WHERE student_id=? AND question_id=?",
                        (student["id"], q["id"]))
            existing = cur.fetchone()
            if existing:
                print(f"  - {q['name']} [existant: {existing['value']} | {existing['comment'] or ''}]")
                edit = input("    Modifier ? (o/N): ").strip().lower()
                if edit != "o":
                    continue
            else:
                print(f"  - {q['name']}")
            val = prompt_value()
            comment = input("    Commentaire (optionnel): ").strip()
            if existing:
                cur.execute("UPDATE note SET value=?, comment=? WHERE student_id=? AND question_id=?",
                            (val, comment if comment else None, student["id"], q["id"]))
            else:
                cur.execute("INSERT INTO note(student_id, question_id, value, comment) VALUES (?, ?, ?, ?)",
                            (student["id"], q["id"], val, comment if comment else None))
            conn.commit()
    print("\nSaisie terminée.")

def compute_for_student(conn, student_id):
    # Retourne (final_20_arrondi, final_20_brut, details)
    cur = conn.cursor()
    # Récup parts de l'éval de l'étudiant
    cur.execute("""
        SELECT p.id, p.name, p.max_points
        FROM part p
        JOIN student s ON s.evaluation_id = p.evaluation_id
        WHERE s.id=?
        ORDER BY p.ord ASC
    """, (student_id,))
    parts = cur.fetchall()
    if not parts:
        return None

    total_max = sum(p["max_points"] for p in parts)
    total_score = 0.0
    details = []

    for p in parts:
        cur.execute("SELECT id, name, coefficient FROM question WHERE part_id=? ORDER BY ord ASC", (p["id"],))
        qs = cur.fetchall()
        if not qs:
            part_score = 0.0
            details.append({"part": p, "part_score": part_score, "q": []})
            continue

        coeff_sum = sum(q["coefficient"] for q in qs)
        q_details = []
        weighted = 0.0
        for q in qs:
            cur.execute("SELECT value, comment FROM note WHERE student_id=? AND question_id=?", (student_id, q["id"]))
            n = cur.fetchone()
            value = n["value"] if n else 0.0
            comment = n["comment"] if n else None
            weighted += value * q["coefficient"]
            q_details.append({
                "q": q,
                "value": value,
                "comment": comment
            })
        part_ratio = (weighted / coeff_sum) if coeff_sum > 0 else 0.0
        part_score = p["max_points"] * part_ratio
        total_score += part_score
        details.append({"part": p, "part_score": part_score, "q": q_details})

    final_raw_20 = (total_score / total_max) * 20 if total_max > 0 else 0.0
    final_round_20 = round_half_nearest(final_raw_20)
    return final_round_20, final_raw_20, details

def modulation_for_student(conn, eval_id, student):
    # Individualisation (C9) : facteur = charge déclarée / part égale du groupe (100/effectif).
    # Une contribution égale (charge = 100/n) laisse la note inchangée (facteur 1).
    # Retourne (facteur, part_egale, charge). Facteur 1.0 si groupe ou charge absent.
    grp = student["group_name"]
    charge = student["charge"]
    if grp is None or charge is None:
        return 1.0, None, charge
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM student WHERE evaluation_id=? AND group_name=?",
                (eval_id, grp))
    n = cur.fetchone()["c"]
    if n <= 0:
        return 1.0, None, charge
    equal = 100.0 / n
    factor = (charge / equal) if equal > 0 else 1.0
    return factor, equal, charge

def individual_note(final_r, factor):
    return min(20.0, round_half_nearest(final_r * factor))

def cmd_compute(args):
    conn = get_conn()
    init_db(conn)
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return
    students = list_students(conn, eval_id)
    if not students:
        print("Aucun étudiant.")
        return
    for s in students:
        comp = compute_for_student(conn, s["id"])
        if not comp:
            continue
        final_r, final_b, _ = comp
        factor, equal, charge = modulation_for_student(conn, eval_id, s)
        done, total = student_progress(conn, s["id"])
        status = "complet" if done == total and total > 0 else f"{done}/{total}"
        if factor != 1.0:
            indiv = individual_note(final_r, factor)
            print(f"- {s['name']}: groupe {final_r:.1f}/20 × charge {charge:g}% "
                  f"(×{factor:.2f}) = {indiv:.1f}/20 [{status}]")
        else:
            print(f"- {s['name']}: {final_r:.1f}/20 (brut {final_b:.2f}) [{status}]")

def sanitize_filename(name: str) -> str:
    bad = '<>:"/\\|?*'
    out = "".join(c if c not in bad else "_" for c in name)
    return out.replace(" ", "_")

def generate_markdown(conn, student, title, final_r, final_b, details, factor, equal, charge, indiv):
    lines = []
    lines.append(f"# {title} - {student['name']}")
    lines.append("")
    lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if student["group_name"]:
        lines.append(f"- Groupe: {student['group_name']}")
    lines.append(f"- Note de groupe (livrables): {final_r:.1f}/20 (brut {final_b:.2f})")
    if charge is not None and factor != 1.0:
        lines.append(f"- Charge déclarée: {charge:g}% (part égale {equal:g}% → facteur ×{factor:.2f})")
        lines.append(f"- **Note individuelle: {indiv:.1f}/20**")
    else:
        lines.append(f"- **Note finale: {final_r:.1f}/20**")
    lines.append("")
    for d in details:
        p = d["part"]
        lines.append(f"## Partie: {p['name']} (/{p['max_points']})")
        lines.append("")
        if not d["q"]:
            lines.append("_Aucune question définie pour cette partie._")
            lines.append("")
            continue
        # calcul part résumé
        part_score = d["part_score"]
        lines.append(f"Score de la partie: {part_score:.2f} / {p['max_points']}")
        lines.append("")
        lines.append("| Question | Évaluation | Commentaire |")
        lines.append("|---|---:|---|")
        for qd in d["q"]:
            q = qd["q"]
            val = qd["value"]
            com = qd["comment"] or ""
            lines.append(f"| {q['name']} | {val:.2f} | {com} |")
        lines.append("")

    # Conseils / mentions
    lines.append("---")
    lines.append("_Document généré automatiquement._")
    return "\n".join(lines)

def cmd_export(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return
    cur.execute("SELECT * FROM evaluation WHERE id=?", (eval_id,))
    eval_row = cur.fetchone()

    students = list_students(conn, eval_id)
    if not students:
        print("Aucun étudiant.")
        return

    count = 0
    for s in students:
        comp = compute_for_student(conn, s["id"])
        if not comp:
            continue
        final_r, final_b, details = comp
        factor, equal, charge = modulation_for_student(conn, eval_id, s)
        indiv = individual_note(final_r, factor)
        md = generate_markdown(conn, s, eval_row["title"], final_r, final_b, details,
                               factor, equal, charge, indiv)
        fname = f"{sanitize_filename(s['name'])}.md"
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        count += 1
    print(f"{count} fichier(s) Markdown généré(s) dans {OUT_DIR}/")

def cmd_validate(args):
    conn = get_conn()
    init_db(conn)
    cur = conn.cursor()
    eval_id = latest_eval_id(conn)
    if not eval_id:
        print("Aucune évaluation.")
        return
    cur.execute("UPDATE evaluation SET status='validated' WHERE id=?", (eval_id,))
    conn.commit()
    print(f"Évaluation {eval_id} validée. Génération des exports...")
    cmd_export(args)

def cmd_commits(args):
    repo = args.repo
    inside = subprocess.run(["git", "-C", repo, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        print(f"Pas un dépôt Git valide : {repo}")
        return
    ensure_dirs()
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

def build_parser():
    p = argparse.ArgumentParser(prog="eval", description="Gestion d'évaluations (CLI)")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("seed", help="Créer une évaluation pré-remplie avec la grille canonique")
    sp.add_argument("--title", help="Titre de l'évaluation")
    sp.set_defaults(func=cmd_seed)

    sp = sub.add_parser("config", help="Créer une évaluation, parties, questions (manuel)")
    sp.set_defaults(func=cmd_config)

    sp = sub.add_parser("load", help="Charger une liste d'étudiants depuis un fichier texte")
    sp.add_argument("file", help="Chemin du fichier (1 ligne par étudiant : 'Groupe;Nom' ou 'Nom')")
    sp.set_defaults(func=cmd_load)

    sp = sub.add_parser("charge", help="Saisir la charge déclarative (%) par étudiant (C9)")
    sp.set_defaults(func=cmd_charge)

    sp = sub.add_parser("list", help="Lister les étudiants et l'état des notes")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("grade", help="Saisir les évaluations d'un étudiant")
    sp.add_argument("--student-id", type=int, help="ID de l'étudiant")
    sp.add_argument("--student-name", help="Nom exact de l'étudiant")
    sp.set_defaults(func=cmd_grade)

    sp = sub.add_parser("compute", help="Afficher les notes finales calculées")
    sp.set_defaults(func=cmd_compute)

    sp = sub.add_parser("commits", help="Compte-rendu des commits Git par auteur")
    sp.add_argument("--repo", required=True, help="Chemin du dépôt Git de l'étudiant/groupe")
    sp.set_defaults(func=cmd_commits)

    sp = sub.add_parser("export", help="Générer les fichiers Markdown par étudiant")
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("validate", help="Valider l'évaluation et exporter")
    sp.set_defaults(func=cmd_validate)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
