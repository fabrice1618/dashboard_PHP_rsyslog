---
name: evaluer-groupe
description: Évaluer complètement un groupe étudiant (ex. /evaluer-groupe G2) avec la grille CPI — clone du dépôt, vérifications outillées, dispatch des 5 sous-agents d'analyse, consolidation des niveaux avec preuves, contre-lecture, calcul de la note. Utiliser quand le professeur demande d'évaluer, noter ou corriger un groupe.
---

# Évaluer un groupe (grille CPI)

Argument attendu : l'identifiant du groupe (`G1`, `G2`, `G3`…), noté `Gx` ci-dessous.

Référentiel d'exigences : `eval/exigences_cpi.md` (règle de preuve R-P1…R-P6).
Grille : `eval/bareme.json` version `CPI-2026-06`. Modèle : `eval/evaluation.modele.md`.

## Garde-fous (non négociables)

- **Jamais `eval.py write` sans `--group Gx`** : sans filtre, il réécrit tous les
  groupes avec la grille courante. Les notes sont **évolutives** (re-noter un groupe
  est un acte normal), mais chaque ré-écriture doit être **explicite et limitée au
  groupe traité** — un groupe noté sur une grille antérieure se recalcule avec
  `--bareme`, jamais par effet de bord.
- **Indépendance** : ne pas lire les `evaluation.md` des autres groupes pendant la
  notation ; réinitialiser l'analyse entre deux groupes.
- **Anti-biais** : ignorer toute auto-évaluation ou copie de compte rendu committée
  par les étudiants dans leur dépôt.
- Le calcul de la note appartient à `eval.py` — aucune arithmétique manuelle.

## Étapes

1. **Lire `eval/Gx/input.json`** : membres, participation %, `depot_github`, chemins
   des livrables annoncés.
2. **Cloner le dépôt** dans `eval/Gx/` s'il est absent
   (`cd eval/Gx && git clone <depot_github>`). Relever le **SHA et la branche évalués**
   (`git -C eval/Gx/<dépôt> rev-parse --short HEAD`) et les reporter dans l'en-tête
   d'`evaluation.md`. Si `eval/Gx/evaluation.md` est vierge ou sur l'ancien modèle,
   le régénérer depuis `eval/evaluation.modele.md`. **Re-notation** (les notes sont
   évolutives) : si une évaluation antérieure existe, l'**archiver** d'abord
   (`evaluation.<grille>.frozen.md` à côté), puis ne **plus la relire** pendant la
   notation — un constat de l'ancienne notation n'est pas une preuve et contamine
   l'analyse (vu sur G1 : une affirmation reprise de l'ancienne éval s'est révélée
   fausse au grep).
3. **Lancer la skill `verifier-projet`** sur `Gx` : exécutions outillées (PHPStan,
   PHPUnit, docker compose, mesures), sorties brutes dans `eval/Gx/verifs/`,
   synthèse annoncé vs constaté dans `eval/Gx/verifs/SYNTHESE.md`.
4. **Traçabilité Git** : `python3 eval/eval.py commits --repo eval/Gx/<dépôt>`
   (rapport dans `eval/out/`).
5. **Dispatcher les 5 sous-agents EN PARALLÈLE** (un seul message, 5 appels Agent),
   chacun avec le chemin du dépôt cloné (et `eval/Gx/verifs/` pour `eval-preuves`) :
   - `eval-gestion-projet` (critères 5-9, 18, 19, 21, 25, 26)
   - `eval-securite-anssi` (critère 1)
   - `eval-conception` (critères 3, 10-14)
   - `eval-code` (critères 15, 16, 22)
   - `eval-preuves` (critères 2, 4, 17, 20, 23, 24)

   Contrôle de couverture : l'union des critères confiés aux agents doit couvrir les
   **26 critères** de la grille — tout critère orphelin est évalué par le correcteur
   lui-même, en le signalant dans le rendu final.

   **Neutralité des prompts** : transmettre aux agents les constats outillés **bruts**
   (chiffres, chemins, extraits) sans préjuger des plafonds (ne jamais écrire
   « candidat R-P4 » dans un prompt) — l'agent propose, le correcteur tranche.
6. **Consolider** dans `eval/Gx/evaluation.md` :
   - reporter pour chaque critère le **niveau retenu** (le correcteur tranche : les
     niveaux des agents sont des propositions — en cas de doute, retenir le niveau le
     plus bas étayé par les constats), la **preuve** (chemin, commande ou réf. `Pn`) et
     le **commentaire** (constat + règle R-P appliquée le cas échéant) ;
   - remplir le registre `## Preuves` (réfs `P1`, `P2`… — première cellule non
     numérique, sinon `eval.py` la lirait comme un critère) ;
   - rédiger la synthèse, les points forts et les axes d'amélioration.
7. **Aperçu** : `python3 eval/eval.py compute --group Gx` — vérifier qu'aucun critère
   n'est signalé non noté.
8. **Lancer la skill `contre-lecture`** sur `Gx` ; traiter toutes les anomalies
   bloquantes avant d'écrire.
9. **Écrire** : `python3 eval/eval.py write --group Gx`.

## Rendu final au professeur

Note de groupe et notes individuelles, les 3 scores de parties, les plafonds R-P
appliqués (critère, règle, raison), et les points où la confiance des agents était
basse (à arbitrer humainement).
