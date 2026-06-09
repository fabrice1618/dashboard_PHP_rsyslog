# Évaluation des projets étudiants — Mode d'emploi

Ce dossier contient le dispositif d'évaluation des projets « dashboard PHP / rsyslog ».
Ce README est la **procédure opératoire complète** : de la mise en place jusqu'à la
remise d'un bulletin de note par étudiant.

- **Énoncé du projet évalué** : <https://github.com/fabrice1618/dashboard_PHP_rsyslog>
- **Promotion en cours** : G1, G2, G3 (composition dans `groupes.ods`, non publiée).

> ⚠️ **Confidentialité (RGPD).** Les données nominatives ne sont **jamais** publiées :
> `groupes.ods`, les dossiers `G1/ G2/ G3/`, la base `evaluation.db`, le dossier `out/`
> et `roster.txt` sont exclus par `.gitignore`. Ne jamais les committer.

---

## 1. Vue d'ensemble

L'évaluation s'appuie sur **une grille canonique de 24 critères** répartie en deux parties
pondérées, et sur un outil unique, `eval.py`, qui réalise **la saisie et tout le calcul**
(base SQLite locale `eval/evaluation.db`). Aucune arithmétique n'est faite à la main.

| Partie | Critères | Poids | Notée sur |
|---|:--:|:--:|:--:|
| Critères principaux | 1 → 21 | 90 % | /18 |
| Qualité logicielle avancée (POO, PHPStan, tests unitaires) | 22 → 24 | 10 % | /2 |

- La notation se fait **par étudiant**, ce qui permet d'individualiser la note de groupe
  selon la charge déclarée (critère C9).
- Le barème détaillé de chaque critère (niveaux 0 à 4) est décrit dans **`evaluation.md`**.
- Le contexte et les décisions ayant conduit à ce dispositif sont consignés dans
  **`REVUE_EVALUATION.md`**.

### Fichiers du dossier

| Fichier | Rôle |
|---|---|
| `eval.py` | **Outil canonique** : saisie + calcul + export (SQLite). |
| `evaluation.md` | Barème détaillé des 24 critères (référence de notation). |
| `REVUE_EVALUATION.md` | Audit du dispositif et décisions pédagogiques (C1–C9). |
| `CLAUDE.md` | Consignes pour l'assistant lors de l'évaluation. |
| `tools/cpi_eval.py` | Utilitaire d'appoint (lecture du roster, vérification de calcul). |
| `groupes.ods` | **Source de vérité** de la composition des groupes (non publiée). |
| `G1/ G2/ G3/` | Rendus des groupes (non publiés). |
| `out/` | Bulletins Markdown générés, un par étudiant (non publié). |
| `evaluation.db` | Base SQLite produite par `eval.py` (non publiée). |

---

## 2. Prérequis

- **Python 3.8+** (bibliothèque standard uniquement, aucune dépendance à installer).
- **Git** disponible dans le `PATH` (pour le compte-rendu des commits).
- Toutes les commandes ci-dessous se lancent **depuis la racine du dépôt**
  (`/home/fab/cours/dashboard_PHP_rsyslog`), car `eval.py` écrit dans `eval/evaluation.db`
  et `eval/out/` en chemins relatifs.

---

## 3. Échelle de notation

Pour chaque critère, attribuer un **niveau** sur l'échelle **0 / 0,25 / 0,5 / 0,75 / 1**,
homothétique aux 5 niveaux du barème de `evaluation.md` :

| Niveau `evaluation.md` | Valeur saisie | Signification |
|:--:|:--:|---|
| 0 | **0** | Non réalisé, inexistant |
| 1 | **0,25** | Abordé superficiellement, incomplet |
| 2 | **0,5** | Partiellement réalisé (correct + incorrect) |
| 3 | **0,75** | Bien réalisé, erreurs mineures |
| 4 | **1** | Très bien réalisé, complet, conforme |

Chaque critère porte aussi un **coefficient** (défaut **1**), modifiable lors de la
création manuelle d'une évaluation (`eval.py config`).

---

## 4. Procédure d'évaluation pas à pas

> Traiter **chaque projet indépendamment** et réinitialiser l'analyse entre deux projets.

### Étape 0 — Préparer le fichier roster

Créer un fichier `roster.txt` (gitignoré), **une ligne par étudiant** au format
`Groupe;Nom` :

```text
G1;BESSAA Badr
G2;NOM Prénom
G3;NOM Prénom
```

La composition exacte se lit depuis `groupes.ods` :

```bash
python3 eval/tools/cpi_eval.py roster
```

### Étape 1 — Créer la grille

```bash
python3 eval/eval.py seed
```

Crée une évaluation pré-remplie avec les 24 critères (coef 1, parties /18 + /2).
Option `--title "…"` pour personnaliser le titre.

### Étape 2 — Charger les étudiants

```bash
python3 eval/eval.py load roster.txt
```

Format accepté par ligne : `Groupe;Nom`, `Groupe<TAB>Nom`, ou simplement `Nom`.

### Étape 3 — Saisir la charge déclarée (individualisation C9)

```bash
python3 eval/eval.py charge
```

Saisir, pour chaque étudiant, sa **charge déclarée en %** (issue du tableau de
répartition exigé par l'énoncé). L'outil **avertit** si la somme des charges d'un
groupe ne fait pas 100 %. Laisser vide pour ne pas modifier.

> Étape facultative : sans charge saisie, la note individuelle = note de groupe.

### Étape 4 — Noter chaque étudiant

```bash
python3 eval/eval.py grade                       # choix interactif de l'étudiant
python3 eval/eval.py grade --student-id 3        # ciblage par id
python3 eval/eval.py grade --student-name "BESSAA Badr"
```

Pour chaque critère : saisir le niveau (0 / 0,25 / 0,5 / 0,75 / 1) et un commentaire
facultatif. Une note déjà saisie peut être révisée (`Modifier ? (o/N)`).
Suivre la progression avec :

```bash
python3 eval/eval.py list
```

### Étape 5 — Traçabilité des commits (critère 20)

```bash
python3 eval/eval.py commits --repo <chemin_du_depot_du_groupe>
```

Produit `eval/out/commits_<dépôt>.md` : nombre de commits et part par auteur
(hors merges), puis le détail des commits par auteur. Sert à objectiver la
contribution individuelle et à noter le critère 20.

### Étape 6 — Vérifier puis exporter

```bash
python3 eval/eval.py compute     # aperçu des notes (groupe + individuelle)
python3 eval/eval.py export      # un bulletin Markdown par étudiant dans eval/out/
```

`validate` fige l'évaluation (`status = validated`) **et** lance l'export :

```bash
python3 eval/eval.py validate
```

---

## 5. Calcul de la note finale

Le calcul est **entièrement délégué à `eval.py`** — jamais à la main.

1. **Score d'une partie** = moyenne des niveaux **pondérée par les coefficients**,
   multipliée par le maximum de la partie (18 ou 2).
2. **Note de groupe /20** = somme des deux parties, ramenée sur /20 et **arrondie au
   0,5 le plus proche** (`round_half_nearest` ; ex. 14,1 → 14,0 ; 14,3 → 14,5).
3. **Note individuelle (C9)** = `note_groupe × (charge_déclarée ÷ part_égale)`,
   où `part_égale = 100 % ÷ effectif du groupe`, **plafonnée à 20** puis arrondie au 0,5.
   Une contribution égale (charge = part égale) laisse la note inchangée (facteur ×1).

> Sans charge saisie, le facteur vaut 1 et le bulletin affiche « **Note finale** »
> (= note de groupe) au lieu de « **Note individuelle** ».

---

## 6. Format de sortie

`export` produit `eval/out/<Nom>.md` par étudiant :

```markdown
# <Titre> - <Nom>

- Date: <horodatage>
- Groupe: <G…>
- Note de groupe (livrables): <X>/20 (brut <X.XX>)
- Charge déclarée: <c>% (part égale <p>% → facteur ×<f>)
- **Note individuelle: <Y>/20**

## Partie: Critères principaux (/18)

Score de la partie: <s> / 18

| Question | Évaluation | Commentaire |
|---|---:|---|
| 1. Analyse des recommandations ANSSI | 0.75 | … |
| … | … | … |

## Partie: Qualité logicielle avancée (10 %) (/2)
…
```

---

## 7. Aide-mémoire des commandes

```bash
# Composition des groupes (depuis groupes.ods)
python3 eval/tools/cpi_eval.py roster

# Pipeline d'évaluation (depuis la racine du dépôt)
python3 eval/eval.py seed                    # crée la grille (24 critères, /18 + /2)
python3 eval/eval.py load roster.txt         # étudiants (1 par ligne : "Groupe;Nom")
python3 eval/eval.py charge                   # charge déclarée (%) par étudiant (C9)
python3 eval/eval.py grade                    # saisie des niveaux 0 / 0,25 / 0,5 / 0,75 / 1
python3 eval/eval.py list                     # état de complétude de la saisie
python3 eval/eval.py commits --repo <dépôt>   # compte-rendu des commits par auteur
python3 eval/eval.py compute                  # aperçu des notes
python3 eval/eval.py export                   # bulletins Markdown dans eval/out/
python3 eval/eval.py validate                 # fige l'évaluation puis exporte
```

> `eval.py config` permet de bâtir une grille **manuelle** (parties, questions,
> coefficients) au lieu de la grille `seed`.

---

## 8. Utilitaire `tools/cpi_eval.py`

Outil d'appoint, sans dépendance, désormais cantonné à :

```bash
python3 eval/tools/cpi_eval.py roster      # lire la composition des groupes
python3 eval/tools/cpi_eval.py selftest    # auto-test du moteur de calcul
python3 eval/tools/cpi_eval.py note --scores "4,4,3,...,0"   # 19 notes (0..4) -> /20
python3 eval/tools/cpi_eval.py skeleton    # (re)générer les squelettes G*/eval.md
```

`cpi_eval.py` applique l'**ancienne** formule par groupe (19 critères, notes 0–4) :
il sert au contrôle de cohérence et à la lecture du roster, **pas** à la notation
officielle, qui passe par `eval.py`.

---

## 9. Références

- **`evaluation.md`** — barème détaillé, niveau par niveau, des 24 critères.
- **`REVUE_EVALUATION.md`** — audit du dispositif et décisions C1–C9.
- **Énoncé** — <https://github.com/fabrice1618/dashboard_PHP_rsyslog>.
