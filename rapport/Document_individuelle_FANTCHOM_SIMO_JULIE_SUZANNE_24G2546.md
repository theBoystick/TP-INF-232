# Documentation individuelle — FANTCHOM SIMO JULIE SUZANNE — 24G2546

## Rôle dans le groupe

J'étais en charge de la **Question 1 : analyse univariée** de la variable `note_evaluation`. Mon travail consistait à décrire statistiquement la distribution des notes des 200 élèves (tendance centrale, dispersion, valeurs atypiques) et à produire les graphiques associés pour le rapport.

## Fichier(s) de code réalisés

**Fichier :** `02_stat_univariee.py`

Fonctions principales :

- `charger_donnees()` — lit `dataset.csv` et nettoie les données (encodage, valeurs manquantes ou mal formées).
- `calculer_statistiques()` — calcule moyenne, médiane, écart-type, variance, min/max, quartiles et IQR.
- `detecter_valeurs_atypiques()` — applique la règle de Tukey pour repérer les notes anormalement faibles ou fortes.
- `tracer_histogramme()` et `tracer_boxplot()` — génèrent les deux graphiques dans `figures/`.
- `analyse_univariee()` — fonction principale qui enchaîne toutes les étapes et affiche le résumé.

## Explication simple du code

Le script commence par charger le fichier `dataset.csv` généré par la partie génération des données. Il vérifie que la colonne `note_evaluation` existe et que les valeurs sont bien numériques, en écartant proprement toute ligne invalide sans faire planter le programme.

Ensuite, il calcule les indicateurs statistiques classiques (moyenne, médiane, quartiles, écart-type). Pour repérer les élèves ayant une note anormale, j'ai utilisé la règle de Tukey : je calcule l'écart interquartile (IQR = Q3 − Q1), puis je considère comme atypique toute note en dehors de l'intervalle [Q1 − 1,5×IQR ; Q3 + 1,5×IQR]. C'est une méthode statistique standard, plus objective qu'un seuil fixé à l'œil.

Enfin, le script produit un histogramme (avec la moyenne et la médiane indiquées par des lignes verticales) et une boîte à moustaches, tous deux sauvegardés en image dans le dossier `figures/` pour être insérés dans le rapport final.

## Résultat obtenu

Sur les 200 élèves du jeu de données du groupe (graine du chef) :

| Indicateur        | Valeur        |
| :---------------- | :------------ |
| Moyenne           | 13,04         |
| Médiane           | 13,25         |
| Écart-type        | 3,47          |
| Q1 / Q3           | 10,67 / 15,62 |
| IQR               | 4,95          |
| Min / Max         | 3,96 / 20,00  |
| Valeurs atypiques | Aucune        |

La distribution est globalement symétrique (moyenne et médiane très proches) et aucune note ne sort de l'intervalle de Tukey [3,25 ; 23,04].

## Difficultés rencontrées

La principale difficulté a été de m'assurer que mon script lise correctement le fichier généré par la partie de KENGNE, DAHA et NKOH : le nom du fichier (`dataset.csv`) et son emplacement (racine du projet, pas de dossier `data/`) ne correspondaient pas exactement à ce qui était prévu dans le cahier des charges initial, donc j'ai dû ajuster mon script en conséquence pour que tout s'exécute correctement.

J'ai aussi dû réfléchir à la meilleure façon de détecter les valeurs atypiques : plutôt que de fixer un seuil arbitraire, j'ai choisi la règle de Tukey (1,5×IQR) qui est la méthode enseignée en cours et largement reconnue en statistique descriptive.

## Ce que je dois savoir expliquer à l'oral

1. La moyenne et la médiane des notes sont très proches (13,04 et 13,25), ce qui montre une distribution symétrique.
2. L'écart-type de 3,47 indique une dispersion modérée : la plupart des notes se situent entre 10 et 16.
3. La règle de Tukey (Q1 − 1,5×IQR ; Q3 + 1,5×IQR) sert à détecter les valeurs atypiques de façon objective.
4. Aucune valeur atypique n'a été trouvée, ce qui s'explique par la génération des notes (bornées entre 0 et 20 avec un bruit contrôlé).
5. Ces résultats servent de base de comparaison pour les questions suivantes (corrélation avec les heures de travail, clustering, classification).
