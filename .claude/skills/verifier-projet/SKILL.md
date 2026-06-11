---
name: verifier-projet
description: Exécuter les vérifications outillées d'un dépôt étudiant cloné (PHPStan, PHPUnit, docker compose, smoke tests, mesures de performance, traçabilité Git) et archiver les sorties brutes dans eval/Gx/verifs/. Utiliser avant toute notation, ou quand le professeur demande de vérifier les affirmations d'un rendu.
---

# Vérifier un projet étudiant (machine à preuves)

Argument attendu : l'identifiant du groupe (`Gx`) ou le chemin du dépôt cloné
(`eval/Gx/<dépôt>`).

Objectif : produire les **constats bruts** qui serviront de preuves à la notation
(règle R-P1 de `eval/exigences_cpi.md` : un niveau ≥ 0,75 exige un artefact vérifié).
Chaque vérification qui échoue est un constat en soi — ne jamais maquiller un échec.

## Règles

- Toutes les sorties sont archivées dans `eval/Gx/verifs/` (gitignoré, RGPD), une par
  fichier : `<AAAAMMJJ-HHMM>_<outil>.txt`. Les écritures restent **confinées** à ce
  dossier — ne jamais modifier le dépôt étudiant.
- Exécuter les commandes depuis le dépôt cloné ; capturer stdout **et** stderr.
- Si un outil est absent de l'environnement (extension PHP manquante…), consigner
  l'échec et sa cause dans le fichier de sortie — c'est un constat, pas un blocage.
- **Ne jamais écraser la sortie d'une tentative échouée** : en cas de ré-exécution,
  suffixer le fichier (`_tentative2`) ou ajouter à la suite — un échec est un constat
  qui doit rester archivé (même s'il est environnemental, le dire dans le fichier).
- **Conflit de ports hôte** (port du compose étudiant déjà occupé) : ne **jamais**
  éditer les fichiers de l'étudiant (pas de `sed` sur `docker-compose.yml`). Créer un
  override **dans `verifs/`** (ex. `eval/Gx/verifs/ports.override.yml` remappant les
  seuls ports en conflit) et lancer
  `docker compose -f docker-compose.yml -f ../verifs/ports.override.yml up -d` ;
  consigner le remap dans le fichier de sortie (les ports internes restent inchangés,
  le constat de déploiement reste valide).

## Vérifications

1. **Dépendances** : `composer install` (ou via le conteneur du projet si fourni).
2. **PHPStan** : `vendor/bin/phpstan analyse` — consigner le **niveau effectif**
   (`phpstan.neon`) et le **nombre exact d'erreurs**. C'est ce constat qui fait foi
   pour le critère 23 (R-P4 si le rendu affirme « sans erreurs »).
3. **PHPUnit** : `vendor/bin/phpunit` — consigner tests passés / échoués / erreurs
   (résultats réels, pas une analyse syntaxique).
4. **Déploiement** : `docker compose up -d` puis `docker compose ps` ; **smoke tests
   HTTP** sur les ports annoncés (`curl -s -o /dev/null -w '%{http_code}' …`) ;
   rejouer **1 à 2 scénarios du plan de recette** du rendu (étapes, résultat constaté) ;
   terminer par `docker compose down -v`.
5. **Performances** : lire le tableau de performances du rendu et **reproduire au
   moins la mesure clé** (ex. `time curl` sur le dashboard, injection de N logs via
   `logger`, comptage en base). Consigner protocole, valeurs et conditions.
6. **Traçabilité** : `git shortlog -sne --no-merges`, dates et rythme des commits
   (`git log --date=short --pretty='%ad %an %s'`).
7. **Synthèse** : produire `eval/Gx/verifs/SYNTHESE.md` — tableau **annoncé vs
   constaté** (affirmation du rendu, source, constat, fichier de preuve). C'est
   l'entrée principale de l'agent `eval-preuves`.
   **Règle de citation** : toute ligne marquée « CONTREDIT » cite le **chemin:ligne du
   dépôt où l'affirmation est réellement écrite**, vérifié par `grep` au moment de la
   rédaction. Affirmation introuvable dans le dépôt ⇒ pas de « CONTREDIT » (reformuler
   en constat neutre) — ne jamais reprendre une affirmation de mémoire ou d'une
   évaluation antérieure (vu sur G1 : « code sans erreurs PHPStan » attribué au rendu
   alors que le dépôt disait l'inverse).

## Rendu

Lister les fichiers produits dans `verifs/` et résumer les écarts annoncé/constaté
détectés (sans proposer de niveaux : c'est le rôle des agents d'évaluation).
