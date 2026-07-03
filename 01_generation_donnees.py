import random
import csv
#import pandas as pd
from config_seed import GRAINE

#print("Graine du groupe :", GRAINE)

def generer_dataset(graine: int, n: int = 200):
    generateur = random.Random(graine)  # générateur LOCAL, isolé
    
    donnees = []
    for i in range(n):
        #    heures_travail (générée en premier) 
        # Heures de travail personnel par semaine, entre 0 et 25h
        heures_travail = generateur.gauss(10, 5)
        heures_travail = max(0, min(25, heures_travail))
        
        #   note_evaluation (corrélée à heures_travail + bruit) 
        # Relation linéaire plausible : note de base 8, +0.5 par heure de travail, + bruit
        bruit_note = generateur.gauss(0, 2.5)
        note = 8 + 0.5 * heures_travail + bruit_note
        note = round(max(0, min(20, note)), 2)
        heures_travail = round(heures_travail, 2)
        
        #   orientation (aléatoir controlé) 
        # Score combinant note (poids fort) et heures (poids faible), + bruit indépendant
        score = 0.7 * note + 0.1 * heures_travail + generateur.gauss(0, 3)
        # Seuil calé empiriquement (score moyen ~10.2) pour un partage réaliste
        orientation = "scientifique" if score >= 10.2 else "litteraire"
        
        donnees.append({
            "id_eleve": f"E{i+1:03d}",
            "note_evaluation": note,
            "heures_travail": heures_travail,
            "orientation": orientation
        })
    
    return donnees


jeu_de_donnees = generer_dataset(graine=GRAINE)
#print("Exemple de données générées :", jeu_de_donnees[:5])  # Affiche les 5 premières entrées

with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id_eleve", "note_evaluation", "heures_travail", "orientation"])
        writer.writeheader()
        writer.writerows(jeu_de_donnees)

print("\nFichier exporté : dataset.csv")



"""
# Chargement des données
df1 = pd.read_csv('dataset_theme_D.csv')
df2 = pd.read_csv('dataset_theme_D1.csv')

# Vérification d'égalité stricte
sont_identiques = df1.equals(df2)
print(f"Les tableaux sont identiques : {sont_identiques}")
"""