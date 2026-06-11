# Évaluation Groupe <Gx> — <titre du projet>

- **Groupe** : <Gx>
- **Membres** (cf. `input.json`) :
  - <NOM Prénom> — participation <xx> %
- **Dépôt évalué** : <url GitHub>
- **Commit évalué** : `<sha>` (branche `<branche>`)
- **Date** : <AAAA-MM-JJ>
- **Grille** : `eval/bareme.json` version `CPI-2026-06` (28 critères, 4 parties pondérées /6 + /5 + /4 + /5)
- **Vérifications outillées** : `eval/<Gx>/verifs/` du <AAAA-MM-JJ> (skill `verifier-projet`)
- **Périmètre** : <ex. dépôt Git uniquement>

> Rappel du barème par critère — **0** non réalisé · **0,25** superficiel · **0,5** partiel ou **non prouvé** · **0,75** bien réalisé, **preuve vérifiée** · **1** complet et conforme, preuves à l'appui.
> Règle de preuve (`eval/exigences_cpi.md`) : R-P1 niveau ≥ 0,75 ⇒ preuve vérifiée · R-P2 déclaratif ⇒ plafond 0,5 · R-P3 reformulation sans source ⇒ plafond 0,5 · R-P4 affirmation contredite ⇒ plafond 0,25 · R-P5 preuve citée · R-P6 hors dépôt = inexistant.

<!-- eval:calcul début — généré par eval.py (python3 eval/eval.py write) ; ne pas éditer à la main -->
<!-- eval:calcul fin -->

## Synthèse

_<2 à 4 phrases : ce que fait le projet, niveau global, ce qui plafonne la note.>_

## Détail — A. Analyse et gestion de projet (/6)

Saisir la colonne **Niveau** (0 / 0,25 / 0,5 / 0,75 / 1) ; `eval.py` calcule la note.
La colonne **Preuve** cite l'artefact (chemin, commande, ou réf. `Pn` du registre `## Preuves`) — obligatoire pour tout niveau ≥ 0,75 (R-P5).

| # | Critère | Niveau | Preuve | Commentaire |
|---|---|:--:|---|---|
| 1 | Analyse des recommandations ANSSI | | | |
| 5 | Contexte initial du projet | | | |
| 6 | Besoins exprimés (expression du besoin / évolutions) | | | |
| 7 | Objectifs du projet | | | |
| 8 | Fonctions principales | | | |
| 9 | Tâches détaillées par livrables et par personnes | | | |
| 18 | Contraintes techniques | | | |
| 19 | Matériels et logiciels mis en œuvre | | | |
| 21 | Échanges avec les IA (prompt / résultat) | | | |
| 25 | Gestion des risques | | | |
| 26 | Indicateurs de suivi de projet | | | |

## Détail — B. Conception et réalisation (/5)

| # | Critère | Niveau | Preuve | Commentaire |
|---|---|:--:|---|---|
| 2 | Procédure d'installation et configuration serveur | | | |
| 3 | Documentation utilisateur | | | |
| 10 | UML Use Case | | | |
| 11 | UML diagramme de blocs ou de déploiement | | | |
| 12 | Schéma synoptique du projet | | | |
| 13 | Sitemap des pages | | | |
| 14 | Mockup partiel du projet | | | |
| 15 | Code PHP — Architecture MVC | | | |
| 16 | Programmation modulaire | | | |
| 22 | Programmation orientée objet | | | |

## Détail — C. Vérification et preuve (/4)

| # | Critère | Niveau | Preuve | Commentaire |
|---|---|:--:|---|---|
| 4 | Tests de validation (use cases) | | | |
| 17 | Critères de performances mesurés | | | |
| 20 | Traçabilité des commits par étudiant *(note commune au groupe)* | | | |
| 23 | Utilisation de PHPStan | | | |
| 24 | Tests unitaires | | | |

## Détail — D. Soutenance (/5)

Le niveau (0 / 0,25 / 0,5 / 0,75 / 1) est saisi par le professeur lors de la soutenance.

| # | Critère | Niveau | Commentaire |
|---|---|:--:|---|
| 27 | Présentation orale *(3 pts)* | | |
| 28 | Démonstration du projet *(2 pts)* | | |

## Preuves

Registre des artefacts vérifiés (référencés `Pn` dans la colonne Preuve — la 1re cellule
reste non numérique pour ne pas être lue comme un critère par `eval.py`).

| Réf | Critère(s) | Artefact / commande | Constat |
|---|---|---|---|
| P1 | | | |

## Traçabilité Git

_Cf. `python3 eval.py commits --repo <dépôt>` (rapport généré dans `eval/out/`)._

| Étudiant | Auteur(s) Git | Commits | Contribution |
|---|---|:--:|---|
| | | | |

## Points forts

- _…_

## Axes d'amélioration

- _…_

---
_Niveaux saisis à la main ; note de groupe et notes individuelles calculées par `eval.py` (`python3 eval/eval.py write --group <Gx>`). Grille : `eval/bareme.json` version `CPI-2026-06` (dépôt /15 + soutenance /5 = /20) ; règle de preuve : `eval/exigences_cpi.md`._
