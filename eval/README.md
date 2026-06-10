# Évaluation des projets étudiants — Mode d'emploi

Ce dossier contient le dispositif d'évaluation des projets « dashboard PHP / rsyslog ».
Ce README est la **procédure opératoire complète**, de la mise en place jusqu'à la note
inscrite dans le compte rendu de chaque groupe.

- **Énoncé du projet évalué** : <https://github.com/fabrice1618/dashboard_PHP_rsyslog>
- **Promotion en cours** : G1, G2, G3.

> ⚠️ **Confidentialité (RGPD).** Les données nominatives ne sont **jamais** publiées :
> les dossiers `G1/ G2/ G3/` et le dossier `out/` sont exclus par `.gitignore`.
> Ne jamais les committer.

---

## 1. Vue d'ensemble

L'évaluation s'appuie sur **une grille de 24 critères** répartie en deux parties pondérées,
et sur `eval.py`, **piloté par fichiers** : il lit la grille, la composition des groupes et
les niveaux saisis, calcule la note, et l'écrit dans le compte rendu. **Aucune base de
données, aucune saisie interactive** : tout est dans des fichiers, et le calcul est
**ré-exécutable** autant de fois que voulu.

| Partie | Critères | Poids | Notée sur |
|---|:--:|:--:|:--:|
| Critères principaux | 1 → 21 | 90 % | /18 |
| Qualité logicielle avancée (POO, PHPStan, tests unitaires) | 22 → 24 | 10 % | /2 |

La notation se fait **par groupe** ; la note de groupe est ensuite individualisée selon
la **participation déclarée** de chaque étudiant (lue dans `input.json`).

### Les trois fichiers du calcul

| Fichier | Rempli par | Rôle |
|---|---|---|
| `eval/bareme.json` | enseignant | Grille : parties, critères, **coefficients**, pondérations. |
| `eval/G*/input.json` | **étudiants** | Membres du groupe + **participation %** + dépôt. |
| `eval/G*/evaluation.md` | **correcteur** | **Niveaux** (0 → 1) et commentaires par critère. |

`eval.py compute` lit ces trois fichiers et affiche les notes ; `eval.py write` insère la
note calculée dans chaque `evaluation.md`, dans le bloc délimité par les marqueurs
`<!-- eval:calcul … -->`.

### Fichiers du dossier

| Fichier | Rôle |
|---|---|
| `eval.py` | Calcul piloté par fichiers : `compute` / `write` / `commits`. |
| `bareme.json` | Grille des 24 critères (coefficients, parties /18 + /2). |
| `evaluation.md` | Barème détaillé, niveau par niveau (référence de notation). |
| `evaluation.modele.md` | Modèle vierge de compte rendu par groupe. |
| `input.json.example` | Modèle du fichier que les étudiants remplissent. |
| `REVUE_EVALUATION.md` | Audit historique du dispositif et décisions pédagogiques. |
| `CLAUDE.md` | Consignes pour l'assistant lors de l'évaluation. |
| `G1/ G2/ G3/` | Par groupe : `input.json` + `evaluation.md` + **dépôt cloné** du groupe (non publiés). |
| `out/` | Rapports de commits générés (non publié). |

---

## 2. Prérequis

- **Python 3.8+** (bibliothèque standard uniquement, aucune dépendance à installer).
- **Git** disponible dans le `PATH` (pour le compte-rendu des commits).
- `eval.py` résout ses chemins par rapport à son propre emplacement : il peut être lancé
  **depuis n'importe quel répertoire** (`python3 eval/eval.py …` depuis la racine du dépôt).

---

## 3. Échelle de notation

Pour chaque critère, saisir un **niveau** dans la colonne **Niveau** des tableaux
`## Détail` de `evaluation.md`, sur l'échelle **0 / 0,25 / 0,5 / 0,75 / 1**,
homothétique aux 5 niveaux du barème de `evaluation.md` :

| Niveau `evaluation.md` | Valeur saisie | Signification |
|:--:|:--:|---|
| 0 | **0** | Non réalisé, inexistant |
| 1 | **0,25** | Abordé superficiellement, incomplet |
| 2 | **0,5** | Partiellement réalisé (correct + incorrect) |
| 3 | **0,75** | Bien réalisé, erreurs mineures |
| 4 | **1** | Très bien réalisé, complet, conforme |

Chaque critère porte aussi un **coefficient**, défini dans `eval/bareme.json`.

---

## 4. Procédure d'évaluation pas à pas

> Traiter **chaque projet indépendamment** et réinitialiser l'analyse entre deux projets.

### Étape 0 — Les étudiants renseignent `input.json`

Chaque groupe remplit son `eval/G*/input.json` (modèle : `eval/input.json.example`) :

- **composition du groupe** (nom + prénom de chaque membre) ;
- **participation (%)** de chaque membre — la somme doit faire **100 %** ;
- **dépôt GitHub** du projet ;
- chemins des **livrables** (analyse ANSSI, UML, sitemap, mockup, etc.).

Ces éléments sont des **livrables exigés par l'énoncé**. La participation sert à
individualiser la note (sans elle, chaque étudiant reçoit la note de groupe).

### Étape 1 — Cloner le dépôt du groupe dans `eval/G*/`

Pour relire les rendus, cloner le dépôt indiqué dans `input.json` (`depot_github`)
**à l'intérieur du dossier du groupe**. Le dépôt cloné garde son nom et reste local :
le dossier `eval/G*/` est exclu par `.gitignore`, donc le code des étudiants n'est
**jamais publié** (RGPD).

```bash
cd eval/G1
git clone <depot_github>     # URL lue dans eval/G1/input.json → crée eval/G1/<nom-du-depot>/
cd ../..
```

> Cloner l'URL **du dépôt** (sans suffixe `/tree/<branche>`). Le correcteur dispose
> ainsi du code source sous `eval/G1/<nom-du-depot>/` pour la relecture et pour la
> traçabilité des commits (étape 3).

### Étape 2 — Le correcteur saisit les niveaux dans `evaluation.md`

Partir du modèle `eval/evaluation.modele.md` (déjà en place dans chaque dossier de groupe).
Pour chaque critère, remplir la colonne **Niveau** (0 / 0,25 / 0,5 / 0,75 / 1) et le
**commentaire** dans les tableaux `## Détail`. Rédiger aussi la synthèse, la traçabilité
Git et les points forts / axes d'amélioration.

> Ne pas toucher au bloc entre les marqueurs `<!-- eval:calcul … -->` : il est généré.

### Étape 3 — Traçabilité des commits (critère 20)

```bash
python3 eval/eval.py commits --repo eval/G1/<nom-du-depot>
```

Produit `eval/out/commits_<dépôt>.md` : nombre de commits et part par auteur (hors merges),
puis le détail par auteur. Sert à objectiver la contribution individuelle.

### Étape 4 — Vérifier puis écrire la note

```bash
python3 eval/eval.py compute     # aperçu des notes (groupe + individuelle), sans écrire
python3 eval/eval.py write       # insère la note calculée dans chaque evaluation.md
```

`write` est **idempotent** : on peut le relancer après chaque modification des niveaux ;
il rafraîchit uniquement le bloc `<!-- eval:calcul … -->` (note de groupe, scores par
partie, notes individuelles).

---

## 5. Calcul de la note finale

Le calcul est **entièrement délégué à `eval.py`** — jamais à la main.

1. **Score d'une partie** = moyenne des niveaux **pondérée par les coefficients**
   (définis dans `bareme.json`), multipliée par le maximum de la partie (18 ou 2).
2. **Note de groupe /20** = somme des deux parties, ramenée sur /20 et **arrondie au
   0,5 le plus proche** (`round_half_nearest` ; ex. 14,1 → 14,0 ; 14,3 → 14,5).
3. **Note individuelle** = `note_groupe × (participation ÷ part_égale)`,
   où `part_égale = 100 % ÷ effectif du groupe`, **plafonnée à 20** puis arrondie au 0,5.
   Une contribution égale (participation = part égale) laisse la note inchangée (facteur ×1).

---

## 6. Format de sortie

Le compte rendu est `eval/G*/evaluation.md` lui-même. `write` y (re)génère le bloc calculé :

```markdown
<!-- eval:calcul début … -->

## Note de groupe : **<X,X> / 20** _(brut <X,XX>)_

| Partie | Score | Poids |
|---|:--:|:--:|
| Critères principaux | <s> / 18 | 90 % |
| Qualité logicielle avancée | <s> / 2 | 10 % |

### Notes individuelles (participation)

| Étudiant | Participation | Note individuelle |
|---|:--:|:--:|
| <NOM Prénom> | <p> % | <Y,Y> / 20 |

<!-- eval:calcul fin -->
```

Le reste du fichier (synthèse, tableaux `## Détail`, traçabilité Git, points forts / axes)
est rédigé par le correcteur et **n'est jamais modifié** par `eval.py`.

---

## 7. Aide-mémoire des commandes

```bash
# 1. Les étudiants remplissent eval/G*/input.json (membres + participation %).
# 2. Cloner le dépôt du groupe dans son dossier :
#       cd eval/G1 && git clone <depot_github> && cd ../..   # → eval/G1/<nom-du-depot>/
# 3. Le correcteur saisit les niveaux dans eval/G*/evaluation.md.

python3 eval/eval.py commits --repo eval/G1/<nom-du-depot>   # compte-rendu des commits par auteur
python3 eval/eval.py compute                  # aperçu des notes (sans écrire)
python3 eval/eval.py write                     # écrit la note dans chaque evaluation.md
```

---

## 8. Références

- **`bareme.json`** — grille machine : critères, coefficients, pondérations.
- **`evaluation.md`** — barème détaillé, niveau par niveau, des 24 critères.
- **`evaluation.modele.md`** — modèle de compte rendu par groupe.
- **`REVUE_EVALUATION.md`** — audit historique du dispositif et décisions C1–C9.
- **Énoncé** — <https://github.com/fabrice1618/dashboard_PHP_rsyslog>.
