# Documentation individuelle — CHOUPO FOGAING Rudy Aubin — 24G2708

## Rôle dans le groupe
Responsable de la **Question 4 : Classification supervisée**.  
Je dois prédire automatiquement l'orientation (scientifique ou littéraire) d'un élève à partir de ses données (note d'évaluation et heures de travail), et évaluer la fiabilité de cette prédiction.

---

## Fichier de code réalisé
**`05_classification_supervisee.py`**

Fonctions / blocs principaux :
- Chargement du CSV (`eleves_theme_D.csv`)
- Préparation des features (`note_evaluation`, `heures_travail`) et de la cible (`orientation`)
- Séparation entraînement / test avec `train_test_split`
- Entraînement d'un **Arbre de décision** (`DecisionTreeClassifier`, max_depth=4)
- Calcul de l'exactitude (`accuracy_score`) et de la matrice de confusion
- Affichage du rapport de classification (précision, rappel, F1)
- Importance des variables
- Sauvegarde de 3 graphiques : matrice de confusion, importance des variables, frontière de décision

---

## Explication simple du code

**Étape 1 — Chargement des données**  
Le script lit le fichier CSV généré par les membres 2 et 3 du groupe. Il vérifie que les deux colonnes numériques (`note_evaluation`, `heures_travail`) et la colonne `orientation` sont bien présentes.

**Étape 2 — Encodage de la cible**  
L'orientation est une chaîne de caractères ("scientifique" / "littéraire"). Je la convertis en entier : 1 = scientifique, 0 = littéraire, ce que sklearn attend.

**Étape 3 — Séparation 80/20**  
80 % des élèves (160) servent à entraîner le modèle. Les 20 % restants (40 élèves) servent uniquement à le tester sur des données qu'il n'a jamais vues. L'option `stratify=y` garantit que les deux classes sont représentées proportionnellement dans chaque sous-ensemble.

**Étape 4 — Modèle : Arbre de décision**  
J'ai choisi un arbre de décision (plutôt qu'une régression logistique ou un SVM) parce qu'il est :
- facile à interpréter (on peut lire les règles)
- adapté à de petits jeux de données (200 élèves)
- limité à `max_depth=4` pour éviter le surapprentissage

**Étape 5 — Évaluation**  
- **Exactitude (accuracy)** : 72,50 % → le modèle se trompe sur environ 1 élève sur 4.
- **Matrice de confusion** : montre les vrais positifs, faux positifs, vrais négatifs et faux négatifs pour chaque classe.
- **Rapport détaillé** : précision et rappel par classe.

**Étape 6 — Importance des variables**  
La `note_evaluation` explique 63,55 % de la décision, les `heures_travail` 36,45 %. La note est donc le meilleur prédicteur de l'orientation.

---

## Résultats obtenus

| Indicateur | Valeur |
|---|---|
| Exactitude globale | **72,50 %** |
| Précision — littéraire | 81 % |
| Rappel — littéraire | 79 % |
| Précision — scientifique | 54 % |
| Rappel — scientifique | 58 % |
| Faux positifs scientifique | 6 élèves |
| Faux négatifs scientifique | 5 élèves |
| Importance note_evaluation | 63,55 % |
| Importance heures_travail | 36,45 % |

**Matrice de confusion (jeu de test, 40 élèves) :**

|  | Prédit littéraire | Prédit scientifique |
|---|---|---|
| **Réel littéraire** | 22 | 6 |
| **Réel scientifique** | 5 | 7 |

**Graphiques produits :**
- `figures/confusion_matrix.png`
- `figures/importance_variables.png`
- `figures/frontiere_decision.png`

---

## Difficultés rencontrées

1. **Déséquilibre des classes** : 139 littéraires contre 61 scientifiques. Le modèle est naturellement meilleur sur la classe majoritaire (littéraire). J'ai utilisé `stratify=y` pour atténuer ce biais.
2. **Choix du modèle** : j'ai hésité entre régression logistique et arbre de décision. J'ai retenu l'arbre car il est plus pédagogiquement lisible.
3. **Interprétation du rappel scientifique (58 %)** : cela signifie que sur les vrais scientifiques, le modèle en manque presque la moitié — risque pédagogique non négligeable.

---

## Ce que je dois savoir expliquer à l'oral

1. La **classification supervisée** utilise des exemples étiquetés (orientation connue) pour apprendre un modèle capable de prédire l'étiquette de nouveaux exemples.
2. On **sépare** les données en entraînement et test pour mesurer la généralisation, pas la mémorisation.
3. L'**exactitude** seule ne suffit pas quand les classes sont déséquilibrées : précision et rappel sont complémentaires.
4. La **matrice de confusion** permet de voir précisément quels types d'erreurs le modèle commet (faux positifs vs faux négatifs).
5. Un modèle à 72,50 % peut sembler correct, mais **11 élèves sur 40 sont mal orientés**, ce qui est pédagogiquement inacceptable si la décision est définitive — le modèle doit rester un outil d'aide à la décision humaine.
