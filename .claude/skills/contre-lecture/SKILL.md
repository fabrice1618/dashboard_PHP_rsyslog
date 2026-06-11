---
name: contre-lecture
description: Contre-lire une évaluation remplie (eval/Gx/evaluation.md) avant le calcul de la note — cohérence preuve/niveau (règle R-P5), cohérence avec les vérifications outillées, calibration inter-groupes. Utiliser avant tout eval.py write, ou quand le professeur demande un audit de cohérence des notes.
---

# Contre-lecture d'une évaluation

Argument attendu : l'identifiant du groupe (`Gx`), ou « tous » pour la calibration
inter-groupes de fin de promotion.

Référentiel : `eval/exigences_cpi.md` (R-P1…R-P6). C'est la **seconde lecture** du
dispositif qualité : aucune note n'est écrite (`eval.py write`) tant que des anomalies
bloquantes subsistent.

## Contrôles sur `eval/Gx/evaluation.md`

1. **R-P5 — preuve citée et existante** : pour chaque niveau **≥ 0,75** des tableaux
   `## Détail`, vérifier que la colonne Preuve est renseignée ET que l'artefact existe
   réellement (fichier présent au chemin cité, ligne `Pn` du registre `## Preuves`
   renseignée, fichier de `verifs/` existant). Manquant → **anomalie bloquante**.
2. **Cohérence avec les constats outillés** : pour les critères **4, 17, 23, 24** (et 2),
   confronter le niveau saisi à `eval/Gx/verifs/SYNTHESE.md`. Un niveau ≥ 0,75 alors que
   la synthèse montre un écart annoncé/constaté → anomalie bloquante (R-P2/R-P4).
3. **Plafonds oubliés** : si un commentaire ou un constat d'agent documente un fait
   relevant de R-P2/R-P3/R-P4 mais que le niveau saisi dépasse le plafond → anomalie
   bloquante.
4. **Complétude** : tous les critères de la grille ont un niveau
   (`python3 eval/eval.py compute --group Gx` ne signale aucun critère non noté) ;
   l'en-tête mentionne le SHA évalué et la version de grille.

## Calibration inter-groupes (quand ≥ 2 groupes sont notés)

5. Construire un tableau comparatif des niveaux par critère entre les
   `eval/G*/evaluation.md` **notés avec la même version de grille**. Signaler les
   paires où des constats équivalents ont reçu des niveaux différents (avec citations).
   À ré-exécuter une dernière fois quand toute la promotion est notée.

## Rendu

Liste des anomalies en deux catégories — **bloquantes** (empêchent `write`) et
**signalements** (à l'appréciation du professeur) — chacune avec critère, fait constaté
et correction proposée. Si aucune anomalie : le dire explicitement et donner le feu
vert pour `python3 eval/eval.py write --group Gx`.
