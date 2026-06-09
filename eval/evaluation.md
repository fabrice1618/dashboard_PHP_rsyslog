# Règles d'évaluation des projets étudiants

## Structure d'évaluation

- Il existe un dossier par groupe d'étudiants. La liste des groupes et leur composition fait foi dans `groupes.ods` (commande `python3 tools/cpi_eval.py roster`). Promotion en cours : G1, G2, G3.
- **Procédure**: Traiter chaque projet indépendamment. Réinitialiser l'analyse entre chaque projet.
- **Notation**: Pour chaque critère, attribuer une note de 0 à 4 :
    - **0** : Non réalisé, non traité, inexistant
    - **1** : Abordé superficiellement, incomplet, manque de rigueur
    - **2** : Partiellement réalisé, mélange d'éléments corrects et incorrects
    - **3** : Bien réalisé avec quelques erreurs mineures ou améliorations possibles
    - **4** : Très bien réalisé, complet, conforme aux attentes
- **Livrable**: Créer un fichier `eval.md` dans chaque dossier groupe avec l'évaluation détaillée
- **Note finale**: Proposer une note sur 20 basée sur l'ensemble des critères

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

### 6. Besoins exprimés d'évolution
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

### 17. Programmation orientée objet (BONUS)
**Objectif**: Évaluer l'utilisation des concepts POO

- **4** : Excellent usage de la POO (classes, héritage, encapsulation, polymorphisme)
- **3** : Bonne utilisation des concepts POO
- **2** : Usage basique de la POO
- **1** : Tentative POO avec des erreurs
- **0** : Aucune programmation orientée objet

### 18. Utilisation PHPStan (BONUS)
**Objectif**: Évaluer l'usage des outils d'analyse statique

- **4** : PHPStan configuré et utilisé, code sans erreurs
- **3** : PHPStan configuré, quelques erreurs mineures
- **2** : PHPStan partiellement configuré
- **1** : Tentative d'utilisation PHPStan
- **0** : Aucune utilisation de PHPStan

### 19. Tests unitaires (BONUS)
**Objectif**: Évaluer la mise en place de tests automatisés

- **4** : Tests unitaires complets avec bonne couverture
- **3** : Tests unitaires bien implémentés
- **2** : Tests unitaires basiques
- **1** : Quelques tests unitaires
- **0** : Aucun test unitaire

## Calcul de la note finale

Chaque critère est noté de 0 à 4. Le maximum d'un bloc est donc `nombre_de_critères × 4`.

**Note sur 20** = (Σ des notes des critères 1-16) / (16 × 4) × 20 × 0.9 + (Σ des bonus critères 17-19) / (3 × 4) × 20 × 0.1

- **Critères principaux** (1-16) : 90% de la note → maximum 18/20
- **Critères bonus** (17-19) : 10% de la note → maximum 2/20
- Un sans-faute (19 critères à 4) donne donc 20/20.
- Calcul reproductible et déterministe : `python3 tools/cpi_eval.py note --scores "..."` (19 valeurs 0..4). Ne pas faire l'arithmétique « à la main » / dans le LLM.
- Arrondi : au 0,5 le plus proche (`round_half_nearest`). NB : l'ancien `eval.py` arrondissait au 0,5 supérieur (`ceil`).

## Format du fichier eval.md

```markdown
# Évaluation Groupe [Numéro]

## Critères principaux

### 1. Analyse recommandations ANSSI : [0-4]
[Justification détaillée]

### 2. Procédure installation : [0-4]
[Justification détaillée]

[...pour tous les critères...]

## Critères bonus

### 17. Programmation orientée objet : [0-4]
[Justification détaillée]

[...etc...]

## Note finale proposée : [X]/20

**Calcul** : (Σ critères principaux)/(16 × 4) × 20 × 0.9 + (Σ bonus)/(3 × 4) × 20 × 0.1 = [X]/20

## Points forts
- [Liste des points forts identifiés]

## Points d'amélioration
- [Liste des améliorations suggérées]
```
