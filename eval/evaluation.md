# Règles d'évaluation des projets étudiants

## Structure d'évaluation

- Il existe un dossier par groupe d'étudiants (`eval/G1`, `eval/G2`, `eval/G3`). La composition de chaque groupe fait foi dans son `eval/G*/input.json` (étudiants + participation %, renseigné par les étudiants). Promotion en cours : G1, G2, G3.
- **Outil**: Le calcul est réalisé par `eval.py`, piloté par fichiers (sans base de données). Sources : `eval/bareme.json` (grille), `eval/G*/input.json` (étudiants), `eval/G*/evaluation.md` (niveaux saisis par le correcteur). Modèle de compte rendu : `eval/evaluation.modele.md`.
- **Procédure**: Traiter chaque projet indépendamment. Réinitialiser l'analyse entre chaque projet.
- **Notation**: Pour chaque critère, saisir un niveau dans la colonne **Niveau** des tableaux `## Détail` de `evaluation.md`, sur l'échelle **0 / 0,25 / 0,5 / 0,75 / 1** (homothétique aux 5 niveaux ci-dessous : 0↔0, 1↔0,25, 2↔0,5, 3↔0,75, 4↔1) :
    - **0** : Non réalisé, non traité, inexistant
    - **1** : Abordé superficiellement, incomplet, manque de rigueur
    - **2** : Partiellement réalisé, ou réalisé mais **non prouvé** (plafond du déclaratif)
    - **3** : Bien réalisé, adossé à un **artefact vérifié** par le correcteur
    - **4** : Très bien réalisé, complet, conforme aux attentes, **preuves à l'appui**
- **Exigences CPI (BAC+3)** : le calibrage suit le référentiel `eval/exigences_cpi.md` (règle de preuve, citée dans les commentaires lorsqu'un plafond est appliqué) :
    - **R-P1** : niveau ≥ 0,75 ⇒ artefact vérifiable **et vérifié** par le correcteur
    - **R-P2** : déclaratif non prouvé ⇒ **plafond 0,5**
    - **R-P3** : reformulation sans mapping à la source ⇒ **plafond 0,5**
    - **R-P4** : affirmation contredite par la vérification ⇒ **plafond 0,25**
    - **R-P5** : tout niveau ≥ 0,75 cite sa preuve (colonne Preuve / registre `## Preuves`)
    - **R-P6** : ce qui n'est pas dans le dépôt (ou `eval/G*/verifs/`) n'existe pas pour la notation
- **Livrable**: chaque `eval/G*/evaluation.md` est le compte rendu du groupe ; `python3 eval/eval.py write` y insère la note calculée (bloc entre les marqueurs `<!-- eval:calcul … -->`).
- **Note finale**: Calculée par `eval.py` (`compute` / `write`), jamais « à la main ». Ré-exécutable à volonté. Voir « Calcul de la note finale ».

## Critères d'évaluation détaillés (1–26)

> La répartition des critères en trois parties (A — Analyse et gestion de projet 40 % ·
> B — Conception et réalisation 35 % · C — Vérification et preuve 25 %) et les
> coefficients sont définis dans `eval/bareme.json` (version `CPI-2026-06`).

### 1. Analyse des recommandations ANSSI (Sécurité)
**Objectif**: Vérifier la prise en compte des bonnes pratiques de sécurité

**Preuves attendues** : document citant les recommandations **numérotées** du guide ANSSI journalisation (R1, R4…), avec pour chacune : référence précise, statut (implémentée / planifiée / non applicable justifiée) et pointeur vers l'élément du projet qui l'implémente (fichier de configuration, code).

- **4** : Mapping exhaustif aux recommandations du guide source ; chaque statut « implémentée » est vérifiable dans le dépôt (le correcteur a contrôlé au moins 3 implémentations annoncées) ; arbitrages « non applicable » argumentés par le contexte du projet
- **3** : Mapping au guide source présent et majoritairement exact ; au moins une implémentation annoncée **vérifiée** par le correcteur ; quelques statuts imprécis
- **2** : **Plafond R-P3** — analyse structurée mais constituée de reformulations génériques sans référence aux recommandations sources, OU statuts « implémentés » non vérifiables dans le dépôt
- **1** : Mention superficielle de l'ANSSI, liste de bonnes pratiques génériques
- **0** : Aucune référence aux recommandations ANSSI

### 2. Procédure d'installation et configuration serveur
**Objectif**: Évaluer la clarté et la complétude des instructions de déploiement

**Preuves attendues** : procédure pas-à-pas dans le dépôt ; le correcteur la **rejoue depuis zéro** (skill `verifier-projet`, sorties dans `verifs/`).

- **4** : Procédure complète (prérequis versionnés, configuration des services, permissions/sécurité, vérification du bon fonctionnement), **rejouée avec succès de bout en bout** par le correcteur sans adaptation
- **3** : Procédure bien documentée, rejouée avec succès par le correcteur moyennant des adaptations mineures
- **2** : **Plafond R-P2** — procédure présente mais non rejouée avec succès (étapes manquantes, prérequis implicites), ou jamais rejouable en l'état
- **1** : Instructions basiques, difficiles à suivre
- **0** : Aucune procédure d'installation fournie

### 3. Documentation utilisateur
**Objectif**: Évaluer la qualité de la documentation pour les utilisateurs finaux

**Preuves attendues** : guide dans le dépôt, **captures d'écran réelles** de l'application livrée ; conformité contrôlée par le correcteur sur l'application déployée.

- **4** : Documentation complète et professionnelle (guide détaillé, fonctionnalités, captures réelles, FAQ, rôles utilisateurs), **conforme à l'application livrée** (vérifié par le correcteur)
- **3** : Bonne documentation, conforme à l'application sur les parcours principaux vérifiés ; manques mineurs
- **2** : **Plafond R-P2** — documentation basique, ou non conforme à l'application livrée, ou captures annoncées mais absentes (« à capturer »)
- **1** : Documentation minimale, difficile à utiliser
- **0** : Aucune documentation utilisateur

### 4. Tests de validation basés sur les use cases
**Objectif**: Vérifier la mise en place de tests structurés

**Preuves attendues** : plan de recette (état initial / action / résultat attendu / résultat obtenu) **et** artefacts d'exécution (captures horodatées, extraits de logs, sorties de commandes) ; au moins un scénario rejoué par le correcteur (`verifs/`).

- **4** : Tous les cas d'usage principaux couverts ; chaque « résultat obtenu » est adossé à un artefact ; le correcteur a rejoué **au moins 2 scénarios** avec le résultat annoncé ; les échecs éventuels sont documentés honnêtement
- **3** : Plan structuré et artefacts présents pour la majorité des tests ; **au moins 1 scénario rejoué avec succès** par le correcteur
- **2** : **Plafond R-P2** — plan structuré mais résultats purement déclaratifs (✅ sans artefact), OU artefacts présents mais scénario non reproductible
- **1** : Tests informels, sans structure état/action/attendu/obtenu
- **0** : Aucun test de validation

### 5. Contexte initial du projet
**Objectif**: Évaluer la compréhension et la présentation du contexte

**Preuves attendues** : analyse de l'existant ancrée dans le projet réel (problèmes constatés, éléments factuels), pas un texte générique transposable à n'importe quel projet.

- **4** : Contexte analysé en profondeur : état des lieux factuel, problèmes identifiés et qualifiés, lien explicite avec les choix du projet
- **3** : Contexte bien présenté, ancré dans le projet réel, quelques détails manquants
- **2** : **Plafond R-P3** — contexte décrit mais générique (transposable tel quel à un autre projet), sans ancrage dans l'existant réel
- **1** : Contexte mentionné superficiellement
- **0** : Contexte non défini

### 6. Besoins exprimés (expression du besoin / évolutions)
**Objectif**: Évaluer l'identification des besoins futurs

**Preuves attendues** : besoins priorisés et **traçables** vers les objectifs et fonctions du projet (matrice ou renvois explicites).

- **4** : Besoins clairement identifiés, **priorisés** (méthode explicite, ex. MoSCoW), traçables vers les objectifs/fonctions ; évolutions futures argumentées
- **3** : Bonne identification des besoins principaux avec priorisation, traçabilité partielle
- **2** : Besoins listés mais sans priorisation ni traçabilité vers le reste du dossier
- **1** : Mention superficielle des évolutions
- **0** : Aucune analyse des besoins futurs

### 7. Objectifs du projet
**Objectif**: Vérifier la clarté des objectifs définis

**Preuves attendues** : objectifs SMART dont le caractère « Mesurable » est suivi d'effet : chaque objectif mesurable renvoie à une mesure ou un constat réel en fin de projet (atteint / non atteint / re-planifié).

- **4** : Objectifs SMART et **bilan d'atteinte** en fin de projet : chaque objectif mesurable est confronté au réalisé, les écarts sont expliqués
- **3** : Objectifs SMART bien définis, atteinte vérifiable pour la majorité d'entre eux
- **2** : **Plafond R-P2** — tableau SMART formellement correct mais purement déclaratif : aucune mesure ni bilan d'atteinte (le « M » n'est jamais exercé)
- **1** : Objectifs vagues ou incomplets
- **0** : Objectifs non définis

### 8. Fonctions principales
**Objectif**: Évaluer l'identification et la description des fonctionnalités

**Preuves attendues** : description des fonctions **conforme à l'application livrée** (le correcteur contrôle sur l'application déployée).

- **4** : Fonctions clairement définies, complètes, documentées et **toutes présentes dans l'application livrée** (conformité vérifiée)
- **3** : Bonnes descriptions des fonctions principales, conformité vérifiée sur l'essentiel
- **2** : Fonctions identifiées mais descriptions incomplètes, ou écarts entre l'annoncé et le livré
- **1** : Fonctions mentionnées superficiellement
- **0** : Fonctions non identifiées

### 9. Tâches détaillées par livrables et par personnes
**Objectif**: Évaluer l'organisation et la planification du projet

**Preuves attendues** : planification (tâches par livrable, responsabilités, échéancier, dépendances) **et trace que la planification a vécu** : l'historique Git (dates, jalons) est cohérent avec l'échéancier annoncé.

- **4** : Planification complète (livrables, responsabilités, échéancier réaliste, dépendances) et **cohérente avec l'historique Git** vérifié par le correcteur ; re-planifications documentées
- **3** : Bonne planification, cohérence partielle avec l'historique réel vérifiée
- **2** : **Plafond R-P2** — planification présente mais purement documentaire : aucune trace de suivi réel (échéancier sans rapport avec l'historique, document rédigé en fin de projet)
- **1** : Planification superficielle
- **0** : Aucune planification documentée

### 10. UML Use Case (conformité aux normes UML)
**Objectif**: Évaluer la qualité des diagrammes de cas d'usage

**Preuves attendues** : source du diagramme dans le dépôt (`.puml` ou équivalent) ; cohérence avec les fonctions réellement livrées.

- **4** : Diagrammes conformes (notation correcte, acteurs identifiés, relations `include`/`extend` **sémantiquement justes**), complets et **cohérents avec les fonctions livrées**
- **3** : Bons diagrammes conformes, quelques erreurs mineures de notation ou de sémantique
- **2** : Diagrammes présents mais non conformes aux normes, ou relations sémantiquement incorrectes, ou décalés par rapport au livré
- **1** : Diagrammes basiques, notation incorrecte
- **0** : Aucun diagramme UML use case

### 11. UML Diagramme de blocs ou de déploiement
**Objectif**: Évaluer la modélisation architecturale

**Preuves attendues** : source du diagramme dans le dépôt ; cohérence avec l'infrastructure réellement déployée (`docker-compose.yml`, services, ports — contrôlée par le correcteur).

- **4** : Diagrammes complets et conformes (nœuds, artefacts, protocoles), **fidèles à l'infrastructure réelle** vérifiée
- **3** : Bons diagrammes conformes, cohérence vérifiée sur l'essentiel
- **2** : Diagrammes présents mais incomplets ou en décalage avec le déploiement réel
- **1** : Diagrammes basiques
- **0** : Aucun diagramme architectural

### 12. Schéma synoptique du projet
**Objectif**: Évaluer la vue d'ensemble du système

**Preuves attendues** : schéma dans le dépôt, cohérent avec le système réellement livré (flux, composants, adressage).

- **4** : Schéma complet montrant toutes les interactions système, **fidèle au système livré**, au format outillé (image ou source exportable)
- **3** : Bon schéma cohérent avec le livré, la plupart des éléments présents
- **2** : Schéma partiel, informel, ou en décalage avec le système livré
- **1** : Schéma basique
- **0** : Aucun schéma synoptique

### 13. Diagramme sitemap des différentes pages
**Objectif**: Évaluer l'architecture de l'interface utilisateur

**Preuves attendues** : sitemap dont les pages/routes **existent dans le code livré** (contrôle par le correcteur sur l'arborescence).

- **4** : Sitemap complet et structuré (pages, routes, droits d'accès), **toutes les entrées vérifiées dans le code**
- **3** : Bon sitemap, conformité au code vérifiée sur l'essentiel
- **2** : Sitemap partiel, ou contenant des pages absentes du livré
- **1** : Sitemap basique
- **0** : Aucun sitemap

### 14. Mockup partiel du projet
**Objectif**: Évaluer la conception de l'interface utilisateur

**Preuves attendues** : maquettes dans le dépôt (outil de maquettage ou export image) correspondant aux écrans livrés.

- **4** : Mockups détaillés et professionnels (outil de maquettage), couvrant les écrans clés et **correspondant à l'interface livrée**
- **3** : Bons mockups représentatifs des écrans livrés
- **2** : Mockups basiques (ex. ASCII) ou en décalage avec l'interface livrée
- **1** : Mockups superficiels
- **0** : Aucun mockup

### 15. Code PHP - Architecture logicielle MVC
**Objectif**: Évaluer l'application du pattern MVC

**Preuves attendues** : inspection du code par le correcteur sur **tout** le périmètre livré (toutes les applications du projet, pas seulement la principale).

- **4** : Architecture MVC **homogène sur tout le périmètre** : séparation stricte Model/View/Controller, responsabilités respectées dans chaque application livrée, aucun SQL hors couche Model
- **3** : Bonne application du MVC sur tout le périmètre, écarts mineurs localisés
- **2** : **Plafond** — MVC appliqué sur une partie seulement du périmètre (ex. application principale propre, application secondaire avec SQL dans les contrôleurs), ou erreurs structurelles
- **1** : Structure MVC partielle ou incorrecte
- **0** : Aucune architecture MVC

### 16. Programmation modulaire (fichiers source/fonctions)
**Objectif**: Évaluer l'organisation du code

**Preuves attendues** : inspection du code par le correcteur ; la duplication est recherchée explicitement (fichiers/classes copiés entre applications).

- **4** : Code parfaitement modulaire : séparation logique, fonctions réutilisables, faible couplage / forte cohésion, **aucune duplication** entre composants
- **3** : Bonne modularité, améliorations mineures possibles
- **2** : Modularité partielle, ou duplications de code/fichiers entre applications
- **1** : Tentative de modularité mais code peu organisé
- **0** : Code monolithique, aucune modularité

### 17. Critères de performances mesurés
**Objectif**: Vérifier la définition, la mesure et la vérification d'exigences de performance

**Preuves attendues** : exigences chiffrées **et** protocole de mesure **et** résultats bruts (commande/outil, valeurs, conditions) ; au moins une mesure reproduite par le correcteur (`verifs/`).

- **4** : Exigences chiffrées (temps de réponse, volumétrie, charge), protocole décrit, mesures fournies et écarts analysés ; **mesure clé reproduite par le correcteur** avec un résultat compatible
- **3** : Exigences chiffrées et au moins une mesure réelle documentée et **vérifiée** par le correcteur
- **2** : **Plafond R-P2** — exigences chiffrées mais jamais mesurées (valeurs annoncées sans protocole ni résultat)
- **1** : Mention vague de performances, sans chiffre
- **0** : Aucun critère de performance
- *(R-P4 : une valeur annoncée contredite par la mesure du correcteur sans explication → 0,25 max.)*

### 18. Contraintes techniques
**Objectif**: Évaluer l'identification des contraintes techniques du projet

**Preuves attendues** : contraintes reliées à des choix effectifs du projet (on doit pouvoir vérifier dans le dépôt qu'elles ont été respectées ou arbitrées).

- **4** : Contraintes complètes et justifiées (OS, services, sécurité, compatibilité, réseau), **traçables vers des choix effectifs** du projet
- **3** : Principales contraintes identifiées et justifiées
- **2** : Contraintes partiellement identifiées, ou listées sans justification ni lien avec les choix réels
- **1** : Mention superficielle
- **0** : Aucune contrainte technique identifiée

### 19. Matériels et logiciels mis en œuvre
**Objectif**: Évaluer l'inventaire des moyens matériels et logiciels du projet

**Preuves attendues** : inventaire conforme à ce que le dépôt révèle réellement (Dockerfile, `composer.json`, configurations).

- **4** : Liste complète et précise (versions exactes, rôles), **conforme aux fichiers du projet** vérifiés par le correcteur
- **3** : Liste correcte et conforme, quelques manques (versions partielles)
- **2** : Liste partielle, ou en décalage avec le projet réel
- **1** : Mention superficielle
- **0** : Aucune liste

### 20. Traçabilité des commits par étudiant
**Objectif**: Vérifier la contribution individuelle via l'historique Git (cf. `python3 eval/eval.py commits --repo <dépôt>`)

**Preuves attendues** : rapport `eval/out/commits_*.md` généré par le correcteur ; cohérence avec la participation déclarée dans `input.json` et avec l'échéancier annoncé.

- **4** : Historique clair, commits **réguliers sur toute la durée du projet**, attribuables à chaque étudiant, cohérents avec la répartition déclarée et les jalons annoncés
- **3** : Bonne traçabilité avec quelques déséquilibres ou irrégularités expliqués
- **2** : Traçabilité partielle ou déséquilibrée, ou activité concentrée juste avant le rendu (incohérente avec l'échéancier annoncé)
- **1** : Très peu de commits / attribution floue
- **0** : Aucune traçabilité (pas de dépôt, ou commits non individualisés)

### 21. Échanges avec les IA (prompt / résultat)
**Objectif**: Évaluer la documentation des échanges avec les IA, exigée par l'énoncé

**Preuves attendues** : prompts et résultats **bruts** (pas une synthèse narrative), avec exploitation critique (ce qui a été retenu, rejeté, corrigé, et pourquoi).

- **4** : Échanges bruts documentés et exploités de façon critique ; cohérents avec l'historique du projet (les productions IA se retrouvent dans les commits correspondants)
- **3** : Échanges bruts documentés et utiles, exploitation critique partielle
- **2** : **Plafond R-P2** — synthèse narrative des échanges, sans prompts/résultats bruts, ou échanges fournis sans aucun commentaire critique
- **1** : Échanges anecdotiques ou non commentés
- **0** : Aucun échange fourni

### 22. Programmation orientée objet
**Objectif**: Évaluer l'utilisation des concepts POO

**Preuves attendues** : inspection du code par le correcteur (les concepts doivent être **utilisés à bon escient**, pas plaqués).

- **4** : Usage complet et justifié de la POO : interfaces, classes abstraites, héritage, encapsulation, polymorphisme **effectif**, injection de dépendances — au service de l'architecture
- **3** : Bonne utilisation des concepts POO, usage justifié dans l'ensemble
- **2** : Usage basique de la POO (classes-conteneurs, héritage mécanique)
- **1** : Tentative POO avec des erreurs
- **0** : Aucune programmation orientée objet

### 23. Utilisation PHPStan
**Objectif**: Évaluer l'usage des outils d'analyse statique

**Preuves attendues** : `phpstan.neon` committé, niveau déclaré, et sortie d'exécution. Le correcteur exécute `vendor/bin/phpstan analyse` (skill `verifier-projet`) ; **le nombre d'erreurs constaté fait foi**.

- **4** : Niveau exigeant (≥ 6), **0 erreur à l'exécution par le correcteur**, intégration au workflow (Composer/Makefile/CI), trace d'usage régulier (commits de correction)
- **3** : Configuré à un niveau exigeant, exécution par le correcteur ≤ 5 erreurs mineures, **affirmations du rendu conformes au constat**
- **2** : Configuré et exécutable, mais erreurs nombreuses non corrigées, ou niveau trivial ; affirmations prudentes ou absentes
- **1** : Configuration présente mais non exécutable, ou usage anecdotique
- **0** : Aucune utilisation de PHPStan
- *(R-P4 : toute affirmation « sans erreurs » démentie par l'exécution → 0,25 max.)*

### 24. Tests unitaires
**Objectif**: Évaluer la mise en place de tests automatisés

**Preuves attendues** : tests committés (`phpunit.xml`, bootstrap) et **exécutés par le correcteur** (skill `verifier-projet`) ; les résultats réels font foi.

- **4** : Couverture large (toutes les couches significatives : Model, Service, Controller), **tous les tests passent à l'exécution par le correcteur**
- **3** : Tests bien implémentés, **exécutés par le correcteur et passants** sur le périmètre couvert ; couverture partielle assumée
- **2** : **Plafond R-P2** — tests présents mais non exécutables par le correcteur, ou couverture limitée à une seule couche, ou échecs non documentés
- **1** : Quelques tests unitaires
- **0** : Aucun test unitaire

### 25. Gestion des risques
**Objectif**: Évaluer l'identification, l'évaluation et le suivi des risques du projet — compétence centrale d'un Chef de Projet Informatique

**Preuves attendues** : registre des risques (description, probabilité, impact, criticité, mesure de mitigation, responsable) **et trace de son suivi** : l'historique Git du document montre qu'il a vécu pendant le projet (mises à jour, risques survenus, actions déclenchées).

- **4** : Registre complet (probabilité × impact, mitigation, responsable), **mis à jour pendant le projet** (historique Git vérifié) ; les risques survenus sont documentés avec les actions réellement déclenchées
- **3** : Registre structuré avec évaluation probabilité/impact et mitigations ; au moins une mise à jour en cours de projet vérifiée
- **2** : **Plafond R-P2** — registre présent mais statique : rédigé en une fois (souvent en fin de projet), jamais mis à jour, aucun lien avec les événements réels du projet
- **1** : Risques mentionnés superficiellement, sans évaluation ni mitigation
- **0** : Aucune gestion des risques

### 26. Indicateurs de suivi de projet
**Objectif**: Évaluer le pilotage du projet par indicateurs (prévu/réalisé, jalons, écarts) — un CPI pilote, il ne se contente pas de planifier

**Preuves attendues** : indicateurs d'avancement (prévu vs réalisé, jalons, charge), données réelles **cohérentes avec l'historique des commits**, analyse des écarts et re-planifications.

- **4** : Indicateurs définis et alimentés tout au long du projet (prévu/réalisé, jalons), **cohérents avec l'historique Git vérifié** ; écarts analysés, re-planifications documentées ; rétrospective de fin de projet
- **3** : Indicateurs définis et alimentés avec des données réelles ; cohérence avec l'historique vérifiée sur l'essentiel
- **2** : **Plafond R-P2** — indicateurs définis mais jamais alimentés, ou alimentés avec des valeurs déclaratives incohérentes avec l'historique réel
- **1** : Mention superficielle de l'avancement, sans indicateur
- **0** : Aucun indicateur de suivi

## Calcul de la note finale

Le calcul est entièrement délégué à `eval.py`, à partir des fichiers — **aucune arithmétique manuelle**.

- Chaque critère reçoit un niveau sur l'échelle 0 / 0,25 / 0,5 / 0,75 / 1 (saisi dans `evaluation.md`) et un **coefficient** défini dans `eval/bareme.json` (version `CPI-2026-06`).
- La grille est répartie en **trois parties pondérées** :
    - **A — Analyse et gestion de projet** (1, 5-9, 18, 19, 21, 25, 26) → 40 % de la note, partie notée `/8`.
    - **B — Conception et réalisation** (2, 3, 10-16, 22) → 35 % de la note, partie notée `/7`.
    - **C — Vérification et preuve** (4, 17, 20, 23, 24) → 25 % de la note, partie notée `/5`.
- Pour chaque partie : moyenne des niveaux **pondérée par les coefficients**, multipliée par le maximum de la partie.
- **Note de groupe /20** = somme des deux parties, arrondie au **0,5 le plus proche** (`round_half_nearest`).
- **Note individuelle** = note de groupe × (participation déclarée ÷ part égale du groupe), **plafonnée à 20** puis arrondie au 0,5. Une contribution égale (participation = 100 % ÷ effectif) laisse la note inchangée. La participation est lue dans `input.json` ; la traçabilité Git s'obtient avec `eval.py commits --repo <dépôt>`.

### Déroulé type

```bash
# 1. Les étudiants renseignent eval/G*/input.json (membres + participation %).
# 2. Cloner le dépôt du groupe dans son dossier (lu dans input.json → depot_github) :
#       cd eval/G1 && git clone <depot_github> && cd ../..   # → eval/G1/<nom-du-depot>/
# 3. Le correcteur saisit les niveaux dans la colonne Niveau de eval/G*/evaluation.md.
python3 eval/eval.py commits --repo eval/G1/<nom-du-depot>   # compte-rendu des commits par auteur
python3 eval/eval.py compute --group G2       # aperçu des notes (groupe + individuelle)
python3 eval/eval.py write --group G2         # insère la note calculée dans evaluation.md
```

`write` est **idempotent** : on peut le relancer après chaque modification des niveaux ; il
rafraîchit uniquement le bloc entre les marqueurs `<!-- eval:calcul … -->`.

> ⚠️ **Toujours utiliser `--group`** : sans filtre, `write` réécrit TOUS les `eval/G*/evaluation.md`
> avec la grille courante — y compris les groupes notés avec une grille antérieure.

## Format de sortie

Le compte rendu est `eval/G*/evaluation.md` lui-même. `python3 eval/eval.py write` y (re)génère le
bloc calculé :

```markdown
<!-- eval:calcul début … -->

## Note de groupe : **<X,X> / 20** _(brut <X,XX>)_

| Partie | Score | Poids |
|---|:--:|:--:|
| Analyse et gestion de projet | <s> / 8 | 40 % |
| Conception et réalisation | <s> / 7 | 35 % |
| Vérification et preuve | <s> / 5 | 25 % |

### Notes individuelles (participation)

| Étudiant | Participation | Note individuelle |
|---|:--:|:--:|
| <NOM Prénom> | <p> % | <Y,Y> / 20 |

<!-- eval:calcul fin -->
```

> Le reste du fichier (synthèse, tableaux `## Détail` avec niveaux et commentaires, traçabilité
> Git, points forts / axes) est rédigé par le correcteur et n'est jamais modifié par `eval.py`.
