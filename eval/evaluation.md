# Règles d'évaluation des projets étudiants

## Structure d'évaluation

- Il existe un dossier par groupe d'étudiants (`eval/G1`, `eval/G2`, `eval/G3`). La composition de chaque groupe fait foi dans son `eval/G*/input.json` (étudiants + participation %, renseigné par les étudiants). Promotion en cours : G1, G2, G3.
- **Outil**: Le calcul est réalisé par `eval.py`, piloté par fichiers (sans base de données). Sources : `eval/bareme.json` (grille), `eval/G*/input.json` (étudiants), `eval/G*/evaluation.md` (niveaux saisis par le correcteur). Modèle de compte rendu : `eval/evaluation.modele.md`.
- **Procédure**: Traiter chaque projet indépendamment. Réinitialiser l'analyse entre chaque projet.
- **Notation**: Pour chaque critère, saisir un niveau dans la colonne **Niveau** des tableaux `## Détail` de `evaluation.md`, sur l'échelle **0 / 0,25 / 0,5 / 0,75 / 1** (homothétique aux 5 niveaux ci-dessous : 0↔0, 1↔0,25, 2↔0,5, 3↔0,75, 4↔1) :
    - **0** : Non réalisé, non traité, inexistant
    - **1** : Abordé superficiellement, incomplet, manque de rigueur
    - **2** : Partiellement réalisé, mélange d'éléments corrects et incorrects
    - **3** : Bien réalisé avec quelques erreurs mineures ou améliorations possibles
    - **4** : Très bien réalisé, complet, conforme aux attentes
- **Livrable**: chaque `eval/G*/evaluation.md` est le compte rendu du groupe ; `python3 eval/eval.py write` y insère la note calculée (bloc entre les marqueurs `<!-- eval:calcul … -->`).
- **Note finale**: Calculée par `eval.py` (`compute` / `write`), jamais « à la main ». Ré-exécutable à volonté. Voir « Calcul de la note finale ».

## Critères d'évaluation détaillés

### 1. Analyse des recommandations ANSSI (Sécurité)
**Objectif**: Vérifier la prise en compte des bonnes pratiques de sécurité

- **4** : Analyse complète des recommandations ANSSI avec identification claire des mesures :
  - Recommandations implémentées dans le projet actuel
  - Recommandations planifiées pour les versions futures
  - Recommandations non applicables avec justifications
  - Documentation de l'analyse et des choix
- **3** : Bonne analyse avec la plupart des recommandations traitées
- **2** : Analyse partielle, certaines recommandations identifiées mais incomplètes
- **1** : Mention superficielle des recommandations ANSSI
- **0** : Aucune référence aux recommandations ANSSI

### 2. Procédure d'installation et configuration serveur
**Objectif**: Évaluer la clarté et la complétude des instructions de déploiement

- **4** : Procédure complète, claire et testable :
  - Instructions pas-à-pas détaillées
  - Prérequis système spécifiés
  - Configuration des services (base de données, serveur web, etc.)
  - Gestion des permissions et sécurité
  - Vérification du bon fonctionnement
- **3** : Procédure bien documentée avec quelques détails manquants
- **2** : Procédure présente mais incomplète ou peu claire
- **1** : Instructions basiques, difficiles à suivre
- **0** : Aucune procédure d'installation fournie

### 3. Documentation utilisateur
**Objectif**: Évaluer la qualité de la documentation pour les utilisateurs finaux

- **4** : Documentation complète et professionnelle :
  - Guide d'utilisation détaillé
  - Description des fonctionnalités
  - Captures d'écran/exemples
  - FAQ ou résolution de problèmes courants
  - Documentation des différents rôles utilisateurs
- **3** : Bonne documentation avec la plupart des éléments présents
- **2** : Documentation basique mais utilisable
- **1** : Documentation minimale, difficile à utiliser
- **0** : Aucune documentation utilisateur

### 4. Tests de validation basés sur les use cases
**Objectif**: Vérifier la mise en place de tests structurés

- **4** : Tests complets et rigoureux :
  - État initial clairement défini
  - Actions détaillées étape par étape
  - Résultats attendus précisés
  - Couverture de tous les cas d'usage principaux
  - Documentation des résultats de tests
- **3** : Tests bien structurés pour la plupart des cas d'usage
- **2** : Tests partiels, certains cas couverts
- **1** : Tests basiques ou informels
- **0** : Aucun test de validation

### 5. Contexte initial du projet
**Objectif**: Évaluer la compréhension et la présentation du contexte

- **4** : Contexte clairement exposé et bien analysé
- **3** : Contexte bien présenté avec quelques détails manquants
- **2** : Contexte partiellement décrit
- **1** : Contexte mentionné superficiellement
- **0** : Contexte non défini

### 6. Besoins exprimés (expression du besoin / évolutions)
**Objectif**: Évaluer l'identification des besoins futurs

- **4** : Besoins d'évolution clairement identifiés et priorisés
- **3** : Bonne identification des besoins principaux
- **2** : Besoins partiellement identifiés
- **1** : Mention superficielle des évolutions
- **0** : Aucune analyse des besoins futurs

### 7. Objectifs du projet
**Objectif**: Vérifier la clarté des objectifs définis

- **4** : Objectifs SMART (Spécifiques, Mesurables, Atteignables, Réalistes, Temporels)
- **3** : Objectifs clairs et bien définis
- **2** : Objectifs identifiés mais peu précis
- **1** : Objectifs vagues ou incomplets
- **0** : Objectifs non définis

### 8. Fonctions principales
**Objectif**: Évaluer l'identification et la description des fonctionnalités

- **4** : Fonctions clairement définies, complètes et bien documentées
- **3** : Bonnes descriptions des fonctions principales
- **2** : Fonctions identifiées mais descriptions incomplètes
- **1** : Fonctions mentionnées superficiellement
- **0** : Fonctions non identifiées

### 9. Tâches détaillées par livrables et par personnes
**Objectif**: Évaluer l'organisation et la planification du projet

- **4** : Planification complète :
  - Tâches détaillées par livrable
  - Attribution claire des responsabilités
  - Échéancier réaliste
  - Gestion des dépendances
- **3** : Bonne planification avec quelques détails manquants
- **2** : Planification basique présente
- **1** : Planification superficielle
- **0** : Aucune planification documentée

### 10. UML Use Case (conformité aux normes UML)
**Objectif**: Évaluer la qualité des diagrammes de cas d'usage

- **4** : Diagrammes UML conformes aux normes :
  - Notation UML correcte
  - Acteurs clairement identifiés
  - Cas d'usage complets et cohérents
  - Relations appropriées (include, extend)
- **3** : Bons diagrammes avec quelques erreurs mineures
- **2** : Diagrammes présents mais non conformes aux normes
- **1** : Diagrammes basiques, notation incorrecte
- **0** : Aucun diagramme UML use case

### 11. UML Diagramme de blocs ou de déploiement
**Objectif**: Évaluer la modélisation architecturale

- **4** : Diagrammes techniques complets et conformes
- **3** : Bons diagrammes avec détails suffisants
- **2** : Diagrammes présents mais incomplets
- **1** : Diagrammes basiques
- **0** : Aucun diagramme architectural

### 12. Schéma synoptique du projet
**Objectif**: Évaluer la vue d'ensemble du système

- **4** : Schéma complet montrant toutes les interactions système
- **3** : Bon schéma avec la plupart des éléments
- **2** : Schéma partiel mais utile
- **1** : Schéma basique
- **0** : Aucun schéma synoptique

### 13. Diagramme sitemap des différentes pages
**Objectif**: Évaluer l'architecture de l'interface utilisateur

- **4** : Sitemap complet et bien structuré
- **3** : Bon sitemap avec quelques détails manquants
- **2** : Sitemap partiel
- **1** : Sitemap basique
- **0** : Aucun sitemap

### 14. Mockup partiel du projet
**Objectif**: Évaluer la conception de l'interface utilisateur

- **4** : Mockups détaillés et professionnels
- **3** : Bons mockups représentatifs
- **2** : Mockups basiques mais utiles
- **1** : Mockups superficiels
- **0** : Aucun mockup

### 15. Code PHP - Architecture logicielle MVC
**Objectif**: Évaluer l'application du pattern MVC

- **4** : Architecture MVC bien implémentée :
  - Séparation claire Model/View/Controller
  - Respect des responsabilités de chaque couche
  - Code structuré et maintenable
- **3** : Bonne application du MVC avec quelques écarts
- **2** : Tentative d'application MVC avec des erreurs
- **1** : Structure MVC partielle ou incorrecte
- **0** : Aucune architecture MVC

### 16. Programmation modulaire (fichiers source/fonctions)
**Objectif**: Évaluer l'organisation du code

- **4** : Code parfaitement modulaire :
  - Séparation logique en modules/fichiers
  - Fonctions bien définies et réutilisables
  - Faible couplage, forte cohésion
- **3** : Bonne modularité avec quelques améliorations possibles
- **2** : Modularité partielle
- **1** : Tentative de modularité mais code peu organisé
- **0** : Code monolithique, aucune modularité

### 17. Critères de performances
**Objectif**: Vérifier la définition et la prise en compte d'exigences de performance

- **4** : Critères de performance explicites (temps de réponse, volumétrie de logs, charge supportée) et vérifiés
- **3** : Critères définis et partiellement vérifiés
- **2** : Quelques exigences évoquées sans mesure
- **1** : Mention superficielle
- **0** : Aucun critère de performance

### 18. Contraintes techniques
**Objectif**: Évaluer l'identification des contraintes techniques du projet

- **4** : Contraintes complètes et justifiées (OS, services, sécurité, compatibilité, réseau)
- **3** : Principales contraintes identifiées
- **2** : Contraintes partiellement identifiées
- **1** : Mention superficielle
- **0** : Aucune contrainte technique identifiée

### 19. Matériels et logiciels mis en œuvre
**Objectif**: Évaluer l'inventaire des moyens matériels et logiciels du projet

- **4** : Liste complète et précise (versions, rôles) des matériels et logiciels
- **3** : Liste correcte avec quelques manques
- **2** : Liste partielle
- **1** : Mention superficielle
- **0** : Aucune liste

### 20. Traçabilité des commits par étudiant
**Objectif**: Vérifier la contribution individuelle via l'historique Git (cf. `python3 eval.py commits --repo <dépôt>`)

- **4** : Historique Git clair, commits réguliers et attribuables à chaque étudiant, cohérents avec la répartition déclarée
- **3** : Bonne traçabilité avec quelques déséquilibres
- **2** : Traçabilité partielle ou déséquilibrée
- **1** : Très peu de commits / attribution floue
- **0** : Aucune traçabilité (pas de dépôt, ou commits non individualisés)

### 21. Échanges avec les IA (prompt / résultat)
**Objectif**: Évaluer la documentation des échanges avec les IA, exigée par l'énoncé

- **4** : Échanges (prompts et résultats) documentés, pertinents et exploités de façon critique
- **3** : Échanges documentés et utiles
- **2** : Quelques échanges fournis
- **1** : Échanges anecdotiques ou non commentés
- **0** : Aucun échange fourni

## Critères de qualité logicielle avancée (10 %)

### 22. Programmation orientée objet
**Objectif**: Évaluer l'utilisation des concepts POO

- **4** : Excellent usage de la POO (classes, héritage, encapsulation, polymorphisme)
- **3** : Bonne utilisation des concepts POO
- **2** : Usage basique de la POO
- **1** : Tentative POO avec des erreurs
- **0** : Aucune programmation orientée objet

### 23. Utilisation PHPStan
**Objectif**: Évaluer l'usage des outils d'analyse statique

- **4** : PHPStan configuré et utilisé, code sans erreurs
- **3** : PHPStan configuré, quelques erreurs mineures
- **2** : PHPStan partiellement configuré
- **1** : Tentative d'utilisation PHPStan
- **0** : Aucune utilisation de PHPStan

### 24. Tests unitaires
**Objectif**: Évaluer la mise en place de tests automatisés

- **4** : Tests unitaires complets avec bonne couverture
- **3** : Tests unitaires bien implémentés
- **2** : Tests unitaires basiques
- **1** : Quelques tests unitaires
- **0** : Aucun test unitaire

## Calcul de la note finale

Le calcul est entièrement délégué à `eval.py`, à partir des fichiers — **aucune arithmétique manuelle**.

- Chaque critère reçoit un niveau sur l'échelle 0 / 0,25 / 0,5 / 0,75 / 1 (saisi dans `evaluation.md`) et un **coefficient** défini dans `eval/bareme.json`.
- La grille est répartie en **deux parties pondérées** :
    - **Critères principaux** (1-21) → 90 % de la note, partie notée `/18`.
    - **Qualité logicielle avancée** (22-24 : POO, PHPStan, tests unitaires) → 10 % de la note, partie notée `/2`.
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
python3 eval/eval.py compute                  # aperçu des notes (groupe + individuelle)
python3 eval/eval.py write                    # insère la note calculée dans chaque evaluation.md
```

`write` est **idempotent** : on peut le relancer après chaque modification des niveaux ; il
rafraîchit uniquement le bloc entre les marqueurs `<!-- eval:calcul … -->`.

## Format de sortie

Le compte rendu est `eval/G*/evaluation.md` lui-même. `python3 eval/eval.py write` y (re)génère le
bloc calculé :

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

> Le reste du fichier (synthèse, tableaux `## Détail` avec niveaux et commentaires, traçabilité
> Git, points forts / axes) est rédigé par le correcteur et n'est jamais modifié par `eval.py`.
