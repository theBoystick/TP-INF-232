# **Question 1 — Analyse univariée de la note d'évaluation**

## **1. Objectif**

Cette section étudie la distribution de la variable **note_evaluation** sur les 200 élèves du jeu de données du groupe. L'objectif est de décrire la répartition des notes et de signaler les élèves dont les résultats sont anormalement faibles ou forts.

## **2. Indicateurs calculés**

| Indicateur        | Valeur |
| :---------------- | :----- |
| Effectif          | 200    |
| Moyenne           | 13,04  |
| Médiane           | 13,25  |
| Écart-type        | 3,47   |
| Variance          | 12,05  |
| Minimum           | 3,96   |
| Maximum           | 20,00  |
| Q1 (1er quartile) | 10,67  |
| Q3 (3e quartile)  | 15,62  |
| IQR (Q3 − Q1)     | 4,95   |

## **3. Méthode de détection des valeurs atypiques**

La détection repose sur la **règle de Tukey**, une méthode standard basée sur l'écart interquartile (IQR). Toute note en dehors de l'intervalle :

**[Q1 − 1,5 × IQR ; Q3 + 1,5 × IQR] = [3,25 ; 23,04]**

serait considérée comme atypique. Avec les données du groupe, **aucune note ne sort de cet intervalle** : l'ensemble des 200 notes se situe dans une plage cohérente, sans valeur extrême isolée.

## **4. Interprétation de la distribution**

La moyenne (13,04) et la médiane (13,25) sont très proches, ce qui indique une distribution **globalement symétrique**, sans déformation marquée vers les notes faibles ou fortes.

L'écart-type de 3,47 montre une dispersion modérée : la majorité des élèves obtiennent une note comprise entre 10 et 16 environ (intervalle interquartile), ce qui correspond à un niveau hétérogène mais sans rupture franche entre groupes d'élèves.

L'absence de valeurs atypiques s'explique directement par la méthode de génération des données (documentation de génération) : la note est bornée entre 0 et 20 et construite à partir d'une relation linéaire avec un bruit gaussien modéré, ce qui produit naturellement une distribution régulière sans élève extrême.

## **5. Graphiques produits**

Deux figures ont été générées dans le dossier `figures/` :

- **hist_note_evaluation.png** : histogramme de la distribution des notes, avec la moyenne et la médiane superposées.
- **boxplot_note_evaluation.png** : boîte à moustaches permettant de visualiser les quartiles et l'absence de valeurs atypiques.

L'histogramme fait apparaître une forme proche d'une cloche, centrée autour de 13, cohérente avec le mode de génération des notes (loi normale du bruit ajoutée à une composante linéaire).

## **6. Points clés à retenir (oral)**

1. La distribution des notes est globalement symétrique : moyenne et médiane quasi identiques (13,04 contre 13,25).
2. La dispersion est modérée (écart-type ≈ 3,47), reflétant un niveau hétérogène mais sans rupture nette entre élèves.
3. La règle de Tukey (1,5 × IQR) ne détecte aucune valeur atypique sur les 200 élèves.
4. Cette absence de valeurs extrêmes découle directement de la génération des données : notes bornées entre 0 et 20 avec un bruit gaussien contrôlé.
5. L'intervalle interquartile [10,67 ; 15,62] situe la moitié centrale des élèves, utile comme repère pour comparer avec les résultats des questions suivantes (corrélation, clustering, classification).
6.
