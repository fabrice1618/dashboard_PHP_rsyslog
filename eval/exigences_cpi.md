# Référentiel d'exigences CPI (BAC+3 Chef de Projet Informatique)

Ce document définit le niveau d'exigence appliqué à l'évaluation des projets de la
promotion CPI. Il complète la grille (`eval/bareme.json`, version `CPI-2026-06`) et le
barème détaillé (`eval/evaluation.md`). Il est opposable : chaque plafond appliqué dans
une évaluation cite la règle correspondante (R-P1 à R-P6).

**Principe directeur** : un diplôme de Chef de Projet Informatique certifie la capacité à
**piloter** un projet — analyser, planifier, mesurer, prouver. Au niveau BTS, on évalue
la présence et la qualité apparente des livrables ; au niveau CPI, on évalue la **rigueur
démontrée** : ce qui est affirmé doit être prouvé, ce qui est analysé doit être relié à
ses sources, ce qui est planifié doit être suivi.

## 1. Ce que « niveau CPI » signifie, par domaine

| Domaine | Suffisant en BTS | Exigé en CPI (BAC+3) |
|---|---|---|
| **Analyse** (ANSSI, contexte, besoins) | Le document existe et est structuré | Mapping explicite aux sources (n° de recommandation, citation), arbitrages justifiés, applicabilité argumentée au projet réel |
| **Gestion de projet** | Planning et répartition présents | Risques identifiés et suivis, indicateurs prévu/réalisé, écarts expliqués, jalons tenus ou re-planifiés |
| **Conception** | Diagrammes présents et à peu près conformes | Cohérence inter-diagrammes et diagrammes ↔ code livré ; choix motivés |
| **Code** | Ça fonctionne, structure reconnaissable | Architecture homogène sur **tout** le périmètre, pas de duplication, conventions tenues |
| **Qualité** | Outils installés et configurés | Outils **exécutés par le correcteur**, résultats conformes aux affirmations ; les écarts annoncé/réel sont sanctionnés |
| **Traçabilité** | Des commits existent | Historique cohérent avec la répartition déclarée et avec les échanges IA bruts |

## 2. Règle de preuve

Ces règles s'appliquent à **tous les critères**. Elles sont citées dans la colonne
Commentaire des évaluations lorsqu'un plafond est appliqué.

- **R-P1 — Preuve exigée pour les niveaux hauts** : un niveau **≥ 0,75** exige au moins
  un artefact **vérifiable et vérifié** par le correcteur (commande rejouée, sortie
  d'outil capturée, capture horodatée, mesure reproduite, fichier inspecté avec chemin
  précis).
- **R-P2 — Plafond du déclaratif** : tout élément déclaratif non prouvé (résultat « ✅ »
  sans artefact, performance annoncée sans mesure, affirmation invérifiable) **plafonne
  le critère à 0,5**.
- **R-P3 — Plafond de la reformulation** : une reformulation générique sans mapping à la
  source (ex. « analyse ANSSI » sans référence aux recommandations numérotées du guide)
  **plafonne le critère à 0,5**.
- **R-P4 — Plafond de l'affirmation contredite** : une affirmation **contredite par la
  vérification** du correcteur (ex. « code sans erreurs PHPStan » alors que l'exécution
  en trouve) **plafonne le critère à 0,25** — une affirmation inexacte est une faute de
  rigueur au niveau CPI.
- **R-P5 — Traçabilité de la notation** : tout niveau ≥ 0,75 saisi dans `evaluation.md`
  cite sa preuve dans la colonne **Preuve** (chemin de fichier, commande exécutée, ou
  référence `Pn` du registre `## Preuves`).
- **R-P6 — Périmètre** : ce qui n'est pas dans le dépôt évalué (ou dans les sorties de
  vérification `eval/G*/verifs/`) **n'existe pas** pour la notation.

## 3. Typologie des preuves acceptées

| Domaine | Preuves acceptées |
|---|---|
| Analyse ANSSI | Référence numérotée au guide source + pointeur vers l'élément du projet (fichier de conf, code) qui implémente la mesure, contrôlé par le correcteur |
| Tests de validation | Plan état initial / action / attendu / obtenu **+** artefacts d'exécution (captures horodatées, extraits de logs, sorties de commandes) ; scénario rejoué par le correcteur |
| Performances | Protocole de mesure + résultats bruts (commande, valeurs, conditions) ; mesure clé reproduite par le correcteur (`verifs/`) |
| Qualité logicielle | Sorties `phpstan` / `phpunit` **exécutées par le correcteur** (le nombre d'erreurs constaté fait foi) |
| Déploiement | `docker compose ps` + smoke tests HTTP rejoués par le correcteur |
| Gestion de projet | Historique Git des documents de suivi (le suivi a vécu pendant le projet, pas rédigé la veille du rendu) ; cohérence indicateurs ↔ commits |
| Échanges IA | Prompts et résultats **bruts** (pas une synthèse narrative), avec exploitation critique |
| Traçabilité | `git shortlog -sne`, rythme et dates des commits, cohérence avec la participation déclarée |

## 4. Format de sortie des sous-agents d'évaluation

Chaque sous-agent (`.claude/agents/eval-*.md`) rend, **pour chacun de ses critères**, le
bloc suivant — des faits, pas des opinions :

```
### Critère <id> — <nom>
- Constats : <faits observés, chemins précis>
- Preuves : <chemin:ligne + extrait court, ou commande + sortie>
- Vérifications effectuées : <ce qui a été rejoué/contrôlé>
- Plafond appliqué : <aucun | R-P2/R-P3/R-P4 + raison>
- Niveau proposé : <0 | 0,25 | 0,5 | 0,75 | 1>
- Confiance : <haute | moyenne | basse> — <ce qui manque pour trancher>
```

Le niveau proposé par un agent est une **proposition** : le correcteur tranche lors de la
consolidation, puis la skill `contre-lecture` vérifie la cohérence preuve/niveau avant
tout calcul écrit (`eval.py write --group Gx`).
