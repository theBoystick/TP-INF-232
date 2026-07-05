"""
05_classification_supervisee.py
Responsable : CHOUPO FOGAING Rudy Aubin — Matricule 24G2708
TP INF232 — Thème D : Établissement scolaire secondaire
Question 4 : Classification supervisée de l'orientation (scientifique / littéraire)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)

# ──────────────────────────────────────────────
# 0. Chargement des données
# ──────────────────────────────────────────────
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "eleves_theme_D.csv")
if not os.path.exists(DATA_PATH):
    # Fallback : même dossier que le script
    DATA_PATH = os.path.join(os.path.dirname(__file__), "eleves_theme_D.csv")

df = pd.read_csv(DATA_PATH)
print(f"Données chargées : {len(df)} élèves")
print(df["orientation"].value_counts())
print()

# ──────────────────────────────────────────────
# 1. Préparation des variables
# ──────────────────────────────────────────────
# Variables explicatives (features) : note et heures de travail
X = df[["note_evaluation", "heures_travail"]].values

# Variable cible (label) : orientation — encodée en 0/1
y = (df["orientation"] == "scientifique").astype(int).values
label_names = ["litteraire", "scientifique"]

# ──────────────────────────────────────────────
# 2. Séparation entraînement / test (80 % / 20 %)
# ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"Taille jeu d'entraînement : {len(X_train)} élèves")
print(f"Taille jeu de test        : {len(X_test)} élèves")
print()

# ──────────────────────────────────────────────
# 3. Entraînement du modèle — Arbre de décision
# ──────────────────────────────────────────────
# L'arbre de décision est un modèle simple, interprétable et adapté
# aux petits jeux de données comme le nôtre (200 élèves).
modele = DecisionTreeClassifier(max_depth=4, random_state=42)
modele.fit(X_train, y_train)
print("Modèle entraîné : Arbre de décision (max_depth=4)")
print()

# ──────────────────────────────────────────────
# 4. Évaluation sur le jeu de test
# ──────────────────────────────────────────────
y_pred = modele.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
rapport = classification_report(y_test, y_pred, target_names=label_names)

print(f"=== EXACTITUDE (Accuracy) : {accuracy:.2%} ===")
print()
print("=== MATRICE DE CONFUSION ===")
print(f"{'':20s} Prédit littéraire  Prédit scientifique")
print(f"Réel littéraire     {cm[0][0]:^18d}  {cm[0][1]:^19d}")
print(f"Réel scientifique   {cm[1][0]:^18d}  {cm[1][1]:^19d}")
print()
print("=== RAPPORT DÉTAILLÉ ===")
print(rapport)

# ──────────────────────────────────────────────
# 5. Interprétation pédagogique
# ──────────────────────────────────────────────
vp = cm[1][1]  # vrais positifs scientifique
fp = cm[0][1]  # faux positifs (littéraire prédit scientifique)
fn = cm[1][0]  # faux négatifs (scientifique prédit littéraire)

print("=== INTERPRÉTATION PÉDAGOGIQUE ===")
print(f"  • Le modèle prédit correctement {accuracy:.0%} des orientations.")
print(f"  • {fp} élève(s) littéraires ont été à tort orienté(s) vers scientifique.")
print(f"  • {fn} élève(s) scientifiques ont été à tort orienté(s) vers littéraire.")
print()
print("  RISQUE PÉDAGOGIQUE : une mauvaise orientation peut")
print("  décourager un élève ou l'engager dans une voie inadaptée.")
print("  Ce modèle doit donc rester un OUTIL D'AIDE, non une décision finale.")
print()

# ──────────────────────────────────────────────
# 6. Importance des variables
# ──────────────────────────────────────────────
importances = modele.feature_importances_
noms_vars = ["note_evaluation", "heures_travail"]
print("=== IMPORTANCE DES VARIABLES ===")
for nom, imp in zip(noms_vars, importances):
    print(f"  {nom:25s} : {imp:.2%}")
print()

# ──────────────────────────────────────────────
# 7. Sauvegarde des graphiques
# ──────────────────────────────────────────────
os.makedirs("figures", exist_ok=True)

# -- Graphique 1 : Matrice de confusion --
fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_names)
disp.plot(ax=ax, colorbar=False, cmap="Blues")
ax.set_title("Matrice de confusion — Arbre de décision\n(jeu de test)", fontsize=13)
plt.tight_layout()
plt.savefig("figures/confusion_matrix.png", dpi=150)
plt.close()
print("Graphique sauvegardé : figures/confusion_matrix.png")

# -- Graphique 2 : Importance des variables --
fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(noms_vars, importances, color=["steelblue", "darkorange"])
ax.set_xlabel("Importance relative")
ax.set_title("Importance des variables dans l'arbre de décision", fontsize=12)
for i, v in enumerate(importances):
    ax.text(v + 0.01, i, f"{v:.2%}", va="center", fontsize=10)
plt.tight_layout()
plt.savefig("figures/importance_variables.png", dpi=150)
plt.close()
print("Graphique sauvegardé : figures/importance_variables.png")

# -- Graphique 3 : Frontière de décision --
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                     np.linspace(y_min, y_max, 300))
Z = modele.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

fig, ax = plt.subplots(figsize=(8, 6))
ax.contourf(xx, yy, Z, alpha=0.3, cmap="coolwarm")
colors = ["navy" if yi == 0 else "firebrick" for yi in y]
ax.scatter(X[:, 0], X[:, 1], c=colors, edgecolors="k", linewidths=0.4,
           alpha=0.7, s=50)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="navy", edgecolor="k", label="littéraire"),
    Patch(facecolor="firebrick", edgecolor="k", label="scientifique"),
]
ax.legend(handles=legend_elements, loc="upper left")
ax.set_xlabel("note_evaluation")
ax.set_ylabel("heures_travail")
ax.set_title("Frontière de décision — Arbre de décision", fontsize=13)
plt.tight_layout()
plt.savefig("figures/frontiere_decision.png", dpi=150)
plt.close()
print("Graphique sauvegardé : figures/frontiere_decision.png")

print("\n=== QUESTION 4 TERMINÉE ===")
