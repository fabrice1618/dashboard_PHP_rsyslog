# Revue de la procédure d'évaluation CPI25

> **Objet** : audit du dispositif d'évaluation avant son utilisation sur la nouvelle promotion (G1, G2, G3).
> **Date** : 2026-06-09
> **Périmètre revu** : `evaluation.md` (le « prompt » d'évaluation), `eval.py`, `CLAUDE.md`, `groupes.ods`, confrontés à l'énoncé officiel.
> **Énoncé de référence** : <https://github.com/fabrice1618/dashboard_PHP_rsyslog> (cloné et analysé : `readme.md` + supports ANSSI / rsyslog / UML).

## 0. Résumé exécutif

| # | Constat | Gravité | État |
|:-:|---|:-:|---|
| C1 | **Formule de note cassée** dans `evaluation.md` : un sans-faute donnait **74/20** | 🔴 Critique | ✅ Corrigé |
| C2 | **Deux systèmes de notation incompatibles** coexistent (`evaluation.md` vs `eval.py`) | 🔴 Critique | ⚠️ Recommandation |
| C3 | **Liste de groupes périmée** (`evaluation.md` cite G11–G24) ; promo actuelle = G1–G3 | 🟠 Majeur | ✅ Corrigé |
| C4 | **`CLAUDE.md` décrit l'ancienne promotion** (G11–G24, stacks, IP, identifiants) → biais d'évaluation | 🟠 Majeur | ✅ Atténué |
| C5 | **Arrondi incohérent** : `eval.py` arrondit au 0,5 *supérieur*, la doc dit « au plus proche » | 🟡 Moyen | ✅ Tranché |
| C6 | **Attendus de l'énoncé non couverts** par la grille (perf, contraintes, IA, traçabilité commits…) | 🟡 Moyen | ⚠️ Recommandation |
| C7 | **« Bonus » trompeur** : les critères 17-19 valent 10 % de la note, pas un bonus additif | 🟡 Moyen | ⚠️ Recommandation |
| C8 | **Pondération uniforme** des 16 critères principaux (ANSSI = sitemap) | 🟢 Mineur | ⚠️ Recommandation |
| C9 | **Note de groupe** sans modulation individuelle, alors que l'énoncé exige la répartition par étudiant | 🟡 Moyen | ⚠️ Recommandation |

**Outillage livré pour fiabiliser/reproduire** : `tools/cpi_eval.py` (lecture des groupes, calcul de note déterministe avec self-test, génération des `eval.md`).

---

## 1. Constats critiques

### C1 — La formule de note finale était mathématiquement fausse 🔴

`evaluation.md` notait chaque critère de **0 à 4**, puis calculait :

```
Note/20 = (Σ critères 1-16) / 16 × 20 × 0,9  +  (Σ bonus 17-19) / 12 × 20 × 0,1
```

Le bloc principal divisait par **16** (le *nombre* de critères) au lieu de **16 × 4 = 64** (le *maximum atteignable*). Conséquences chiffrées :

| Scénario | Ancienne formule | Attendu |
|---|:-:|:-:|
| 19 critères à 4 (sans-faute) | **74 / 20** ❌ | 20 / 20 |
| 16 critères principaux à 3, bonus à 0 | **54 / 20** ❌ | 13,5 / 20 |

Le bloc bonus, lui, était correct (`/12 = 3 × 4`). Une note > 20 obligeait le correcteur (humain ou LLM) à « bricoler » mentalement le résultat → **résultat non reproductible**.

**Correction appliquée** (`evaluation.md`) :

```
Note/20 = (Σ critères 1-16) / (16 × 4) × 20 × 0,9  +  (Σ bonus 17-19) / (3 × 4) × 20 × 0,1
```

→ max bloc principal = **18/20**, max bonus = **2/20**, sans-faute = **20/20**. Vérifié par self-test (`python3 tools/cpi_eval.py selftest`).

### C2 — Deux systèmes de notation incompatibles 🔴

Le dépôt contient **deux dispositifs concurrents**, jamais reliés :

| | `evaluation.md` | `eval.py` |
|---|---|---|
| Granularité | par **groupe** | par **étudiant** |
| Échelle | 0, 1, 2, 3, 4 | 0, 0.25, 0.5, 0.75, 1 |
| Critères | 19 critères figés | parties/questions saisies à la main |
| Calcul | formule 90/10 (corrigée) | moyenne pondérée par coefficients |
| Arrondi | 0,5 le plus proche | 0,5 **supérieur** (`ceil`) |
| Sortie | `G*/eval.md` | `eval/out/<nom>.md` |
| Moteur | LLM | interactif (`input()`) |

À noter : les échelles sont en réalité **homothétiques** (0/0.25/0.5/0.75/1 = 0/1/2/3/4 ÷ 4) et **le calcul de `eval.py` est, lui, mathématiquement correct** (il normalise bien sur /20). Mais rien ne dit lequel fait foi : un correcteur qui suit `evaluation.md` ne touchera jamais `eval.py`, et inversement → **ambiguïté de procédure = non-reproductibilité**.

**Recommandation** : choisir **un seul** instrument et le déclarer canonique.
- **Option retenue par défaut dans cette revue** : le pipeline `evaluation.md` + `tools/cpi_eval.py` (par groupe, 19 critères, calcul déterministe). `eval.py` devient *legacy* — à retirer ou à réaligner s'il faut une saisie interactive.
- Si la notation **par étudiant** est requise (cf. C9), repartir de `eval.py` mais le brancher sur les 19 critères de la grille.

---

## 2. Constats majeurs

### C3 — Liste des groupes périmée 🟠

`evaluation.md` annonçait « 8 dossiers G11, G12, G13, G14, G21, G22, G23, G24 ». La promotion à évaluer est **G1, G2, G3** (`groupes.ods`). Risque : un correcteur LLM cherche 8 dossiers inexistants ou se cale sur l'ancienne structure.

**Correction appliquée** : `evaluation.md` pointe désormais vers `groupes.ods` comme source de vérité (`python3 tools/cpi_eval.py roster`) et cite la promo en cours.

Composition lue automatiquement :

| Groupe | Membres |
|---|---|
| G1 | _(composition lue depuis `groupes.ods`, non publiée)_ |
| G2 | _(idem)_ |
| G3 | _(idem)_ |

> La colonne `repository` de `groupes.ods` est **vide** : aucun dépôt étudiant n'est encore rattaché, et les dossiers G1/G2/G3 ne contiennent aucun rendu. Les `eval.md` générés sont donc des **squelettes** prêts à remplir.

### C4 — `CLAUDE.md` induit un biais d'évaluation 🟠

`CLAUDE.md` décrivait en détail l'**ancienne promotion** (CPLR24) : stacks techniques par groupe, adresses IP de VM, identifiants, liens GitHub. Comme ce fichier est injecté dans le contexte de Claude Code à chaque session, il **conditionne le LLM** à attendre NextCloud, telle structure MVC, telles VM… qui n'ont rien à voir avec G1–G3.

**Atténuation appliquée** : l'aperçu de `CLAUDE.md` renvoie à `groupes.ods` + énoncé et signale explicitement que les descriptions G11–G24 sont **historiques et à ignorer**.

**Recommandation complémentaire** : purger ou archiver (dans un fichier séparé `HISTORIQUE_CPLR24.md`) toute la section « Student Project Groups » pour éliminer le biais à la racine.

---

## 3. Couverture : énoncé ↔ grille

Confrontation des **attendus** de l'énoncé (`readme.md`) avec les 19 critères de `evaluation.md`.

### 3.1 Attendus couverts ✅

| Attendu (énoncé) | Critère(s) |
|---|---|
| Analyse livret ANSSI (pris/non pris en compte) | 1 |
| Procédure/documentation d'installation | 2 |
| Documentation utilisateur (cas d'utilisation) | 3 |
| Tests de validation (état initial/action/résultat attendu/obtenu) | 4 |
| Contexte (analyse de l'existant) | 5 |
| Objectif du projet | 7 |
| Fonctions principales | 8 |
| Tâches par livrable / répartition par étudiant | 9 |
| UML use case | 10 |
| UML bloc / déploiement | 11 |
| Schéma réseau / synoptique | 12 |
| Sitemap | 13 |
| Mockup | 14 |
| Architecture MVC | 15 |
| Programmation modulaire | 16 |
| POO (bonus) | 17 |

### 3.2 Attendus de l'énoncé **NON notés** par la grille (C6) 🟡

| Attendu (énoncé) | Statut |
|---|---|
| **Critères de performances** (plan diaporama) | absent de la grille |
| **Contraintes techniques** (plan diaporama) | absent de la grille |
| **Liste matériels et logiciels** mis en œuvre | absent de la grille |
| **Traçabilité des commits par étudiant** (repo GitHub) | absent — pourtant clé pour une note individuelle |
| **Échanges avec les IA (prompt/résultat)** | absent — explicitement exigé par l'énoncé |
| **Démonstration / recette** (10 min) | non noté en tant que tel |
| **Diaporama** (qualité de présentation, 20 min) | non noté en tant que tel |

**Recommandation** : soit ajouter des critères correspondants, soit indiquer explicitement dans `evaluation.md` qu'ils sont hors périmètre de la note écrite (p. ex. évalués à l'oral). Le point « échanges avec les IA » mérite au minimum une mention vu le contexte pédagogique.

### 3.3 Critères de la grille **absents de l'énoncé** (sur-spécification)

| Critère | Remarque |
|---|---|
| 18. PHPStan (bonus) | non demandé par l'énoncé → acceptable en bonus, à assumer |
| 19. Tests unitaires (bonus) | non demandé par l'énoncé → acceptable en bonus, à assumer |

### 3.4 Décalage sémantique — critère 6

La grille intitule le critère 6 « **Besoins exprimés d'évolution** » (besoins *futurs*), alors que l'énoncé demande l'« **expression du besoin** » (besoin *initial*). Ce sont deux notions différentes. Dans `tools/cpi_eval.py` le libellé a été **harmonisé** en « Besoins exprimés (expression du besoin / évolutions) ». **Recommandation** : aligner aussi le titre dans `evaluation.md`, et trancher ce qui est réellement attendu.

---

## 4. Autres constats

### C5 — Politique d'arrondi incohérente 🟡
`eval.py` utilise `ceil_to_half` (arrondi au 0,5 **supérieur** : 14,1 → 14,5), tandis que `CLAUDE.md` documente « rounded to nearest 0.5 ». **Tranché** : `tools/cpi_eval.py` arrondit **au plus proche** (conforme à la spec écrite) et le signale ; `evaluation.md` documente désormais la règle et la divergence de l'ancien `eval.py`.

### C7 — « Bonus » trompeur 🟡
Avec la formule (corrigée), le bloc principal plafonne à **18/20** et les critères 17-19 apportent les **2 derniers points** : ce ne sont donc pas des points *en plus* d'une note sur 20, mais **10 % de la note**. Un groupe parfait sur le fond mais sans POO/PHPStan/tests unitaires est **plafonné à 18/20**. **Recommandation** : soit assumer (renommer « Qualité logicielle avancée — 10 % »), soit faire un vrai bonus additif (note principale sur /20 pleins, bonus ajouté par-dessus et capé).

### C8 — Pondération uniforme 🟢
Les 16 critères principaux pèsent identiquement (5,625 % chacun) : l'analyse ANSSI vaut autant que le sitemap. Si certains critères sont prioritaires, introduire des coefficients (l'`eval.py` legacy en gérait déjà ; `cpi_eval.py` peut être étendu).

### C9 — Note de groupe vs contribution individuelle 🟡
L'énoncé impose un **tableau de répartition de la charge** et la **traçabilité des commits par étudiant**. La grille produit une note **de groupe** unique, sans mécanisme de modulation individuelle. **Recommandation** : si des notes individuelles sont visées, appliquer la répartition (%) déclarée et vérifiée via l'historique Git comme facteur de modulation, ou réutiliser l'approche par étudiant de `eval.py`.

---

## 5. Reproductibilité — ce qui a été mis en place

Objectif demandé : évaluation **fiable et reproductible**. Mesures :

1. **Arithmétique centralisée et testée** — `tools/cpi_eval.py` calcule la note ; le LLM/correcteur ne fait **aucun calcul**. Self-test intégré (5 cas, dont sans-faute = 20). Cela neutralise définitivement le risque C1.
2. **Source de vérité unique pour les groupes** — `groupes.ods`, lu par script (`roster`). `evaluation.md` et `CLAUDE.md` y renvoient au lieu de dupliquer des listes qui se périment.
3. **Squelettes `eval.md` générés** — structure identique pour tous les groupes, barème rappelé, **ligne « Preuve / fichier(s) » imposée par critère** (ancre la note sur une justification vérifiable → moins de variance entre passes).
4. **Biais de contexte neutralisé** — l'ancienne promotion n'est plus présentée comme la référence (C4).
5. **Sans dépendance externe** — script Python *stdlib* only : exécutable à l'identique sur n'importe quelle machine.

### Utilisation

```bash
# Composition des groupes (depuis groupes.ods)
python3 tools/cpi_eval.py roster

# (Re)générer les squelettes eval.md (--force pour écraser)
python3 tools/cpi_eval.py skeleton

# Vérifier le moteur de calcul
python3 tools/cpi_eval.py selftest

# Calculer une note à partir des 19 notes (0..4)
python3 tools/cpi_eval.py note --scores "4,4,3,3,4,2,3,3,2,3,3,2,2,2,3,3,2,0,0"
```

---

## 6. Synthèse des modifications appliquées

| Fichier | Modification |
|---|---|
| `evaluation.md` | Formule corrigée (×4) + bornes 18/2 + note de reproductibilité + règle d'arrondi ; liste de groupes → renvoi à `groupes.ods` |
| `CLAUDE.md` | Aperçu → renvoi `groupes.ods` + promo G1-G3 ; avertissement « descriptions G11-G24 historiques, à ignorer » |
| `tools/cpi_eval.py` | **Nouveau** — roster / note / skeleton / selftest, sans dépendance |
| `G1/eval.md`, `G2/eval.md`, `G3/eval.md` | **Nouveaux** squelettes d'évaluation (roster + grille corrigée) |
| `REVUE_EVALUATION.md` | **Ce rapport** |

## 7. Recommandations restantes (décisions de l'enseignant)

1. **Trancher C2** : déclarer le système canonique (par défaut : `evaluation.md` + `cpi_eval.py`) et retirer/réaligner `eval.py`.
2. **Décider C6** : ajouter des critères pour perf / contraintes techniques / matériels-logiciels / traçabilité commits / échanges IA, ou les marquer hors périmètre.
3. **Décider C7** : « bonus » réellement additif, ou bloc « Qualité logicielle » assumé à 10 %.
4. **Décider C8/C9** : coefficients par critère ? note individualisée ?
5. **Finaliser C4** : déplacer la description CPLR24 vers un `HISTORIQUE_CPLR24.md`.
6. **Renseigner `groupes.ods`** : colonne `repository` (liens des dépôts étudiants) dès réception, pour permettre l'évaluation réelle.

---
_Rapport généré dans le cadre de la revue « Revue + outillage »._
