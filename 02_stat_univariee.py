import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHEMIN_DONNEES = os.path.join(BASE_DIR, "data", "eleves_theme_D.csv")
DOSSIER_FIGURES = os.path.join(BASE_DIR, "figures")
COLONNE = "note_evaluation"


def charger_donnees(chemin=CHEMIN_DONNEES):
    if not os.path.exists(chemin):
        alt = os.path.join(BASE_DIR, "data", "eleves_theme_D.csv")
        if os.path.exists(alt):
            chemin = alt
        else:
            print(f"Erreur : fichier introuvable ({chemin})")
            print("Lance d'abord 01_generation_donnees.py pour creer eleves_theme_D.csv.")
            sys.exit(1)

    try:
        df = pd.read_csv(chemin, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(chemin, encoding="latin-1")

    df.columns = [c.strip() for c in df.columns]

    if COLONNE not in df.columns:
        print(f"Erreur : la colonne '{COLONNE}' n'existe pas dans le fichier.")
        print(f"Colonnes trouvees : {list(df.columns)}")
        sys.exit(1)

    df[COLONNE] = df[COLONNE].astype(str).str.replace(",", ".", regex=False).str.strip()
    df[COLONNE] = pd.to_numeric(df[COLONNE], errors="coerce")

    nb_avant = len(df)
    df = df.dropna(subset=[COLONNE])
    nb_supprimees = nb_avant - len(df)
    if nb_supprimees > 0:
        print(f"Attention : {nb_supprimees} ligne(s) avec une note invalide ont ete ignorees.")

    if df.empty:
        print("Erreur : aucune donnee exploitable dans la colonne note_evaluation.")
        sys.exit(1)

    return df


def calculer_statistiques(serie):
    q1 = serie.quantile(0.25)
    q2 = serie.quantile(0.50)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1

    return {
        "effectif": int(serie.count()),
        "moyenne": serie.mean(),
        "mediane": q2,
        "ecart_type": serie.std(ddof=1) if serie.count() > 1 else 0.0,
        "variance": serie.var(ddof=1) if serie.count() > 1 else 0.0,
        "minimum": serie.min(),
        "maximum": serie.max(),
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "IQR": iqr,
        "borne_basse": q1 - 1.5 * iqr,
        "borne_haute": q3 + 1.5 * iqr,
    }


def detecter_valeurs_atypiques(df, stats):
    masque = (df[COLONNE] < stats["borne_basse"]) | (df[COLONNE] > stats["borne_haute"])
    colonnes_id = "id_eleve" if "id_eleve" in df.columns else df.columns[0]
    return df.loc[masque, [colonnes_id, COLONNE]].sort_values(by=COLONNE)


def tracer_histogramme(serie, stats):
    os.makedirs(DOSSIER_FIGURES, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.hist(serie, bins=12, color="#4C72B0", edgecolor="black", alpha=0.85)
    plt.axvline(stats["moyenne"], color="red", linestyle="--", linewidth=1.5,
                label=f"Moyenne = {stats['moyenne']:.2f}")
    plt.axvline(stats["mediane"], color="green", linestyle="--", linewidth=1.5,
                label=f"Mediane = {stats['mediane']:.2f}")
    plt.title("Distribution des notes d'evaluation")
    plt.xlabel("Note (/20)")
    plt.ylabel("Effectif")
    plt.legend()
    plt.tight_layout()
    chemin = os.path.join(DOSSIER_FIGURES, "hist_note_evaluation.png")
    plt.savefig(chemin, dpi=150)
    plt.close()
    return chemin


def tracer_boxplot(serie):
    os.makedirs(DOSSIER_FIGURES, exist_ok=True)
    plt.figure(figsize=(6, 5))
    plt.boxplot(serie, vert=True, patch_artist=True,
                boxprops=dict(facecolor="#DD8452", color="black"),
                medianprops=dict(color="black", linewidth=2))
    plt.title("Boite a moustaches - Note d'evaluation")
    plt.ylabel("Note (/20)")
    plt.tight_layout()
    chemin = os.path.join(DOSSIER_FIGURES, "boxplot_note_evaluation.png")
    plt.savefig(chemin, dpi=150)
    plt.close()
    return chemin


def afficher_resume(stats, atypiques):
    print("=" * 55)
    print("QUESTION 1 - ANALYSE UNIVARIEE : note_evaluation")
    print("=" * 55)
    print(f"Effectif               : {stats['effectif']}")
    print(f"Moyenne                : {stats['moyenne']:.2f}")
    print(f"Mediane                : {stats['mediane']:.2f}")
    print(f"Ecart-type             : {stats['ecart_type']:.2f}")
    print(f"Variance               : {stats['variance']:.2f}")
    print(f"Min / Max              : {stats['minimum']:.2f} / {stats['maximum']:.2f}")
    print(f"Q1 / Q2 / Q3           : {stats['Q1']:.2f} / {stats['Q2']:.2f} / {stats['Q3']:.2f}")
    print(f"IQR                    : {stats['IQR']:.2f}")
    print(f"Bornes (regle Tukey)   : [{stats['borne_basse']:.2f} ; {stats['borne_haute']:.2f}]")
    print("-" * 55)

    if atypiques.empty:
        print("Aucune valeur atypique detectee.")
    else:
        print(f"{len(atypiques)} valeur(s) atypique(s) :")
        for _, ligne in atypiques.iterrows():
            note = ligne[COLONNE]
            statut = "tres faible" if note < stats["borne_basse"] else "tres forte"
            print(f"  - {ligne.iloc[0]} : note = {note:.2f} ({statut})")
    print("=" * 55)


def analyse_univariee(chemin_donnees=CHEMIN_DONNEES):
    df = charger_donnees(chemin_donnees)
    serie = df[COLONNE]

    stats = calculer_statistiques(serie)
    atypiques = detecter_valeurs_atypiques(df, stats)

    chemin_hist = tracer_histogramme(serie, stats)
    chemin_box = tracer_boxplot(serie)

    afficher_resume(stats, atypiques)
    print(f"\nHistogramme : {chemin_hist}")
    print(f"Boxplot     : {chemin_box}")

    return {
        "statistiques": stats,
        "valeurs_atypiques": atypiques,
        "figures": {"histogramme": chemin_hist, "boxplot": chemin_box},
    }


if __name__ == "__main__":
    analyse_univariee()