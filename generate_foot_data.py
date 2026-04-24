import pandas as pd
import numpy as np

print("⚽ Création du dataset des joueurs de football...")

# Fixer la graine pour avoir toujours les mêmes résultats (Reproductibilité)
np.random.seed(42)
n_samples = 500

# 1. Génération des caractéristiques (Features)
fatigue = np.random.randint(20, 100, n_samples)          # De 20% à 100% de fatigue
sommeil = np.random.uniform(4.0, 10.0, n_samples)        # De 4h à 10h de sommeil
km_courus = np.random.uniform(10.0, 50.0, n_samples)     # Distance parcourue la semaine
douleur = np.random.randint(0, 10, n_samples)            # Douleur musculaire (0 à 10)

# 2. Logique de décision (Target)
# Règle générale : Le joueur est Inapte (0) s'il est trop fatigué, a trop mal, ou dort trop peu.
apte = np.ones(n_samples, dtype=int)
apte[(fatigue > 80) | (douleur >= 7) | (sommeil < 5)] = 0

# Ajout de 5% de "bruit" aléatoire (parce que dans la vraie vie, le corps humain est imprévisible !)
bruit = np.random.choice(n_samples, size=int(0.05 * n_samples), replace=False)
apte[bruit] = 1 - apte[bruit]

# 3. Création du DataFrame et sauvegarde en CSV
df = pd.DataFrame({
    "fatigue": fatigue,
    "sommeil": np.round(sommeil, 1),
    "km_courus": np.round(km_courus, 1),
    "douleur": douleur,
    "Apte_au_match": apte
})

df.to_csv("joueurs_data.csv", index=False)
print("✅ Fichier 'joueurs_data.csv' créé avec succès (500 lignes) !")