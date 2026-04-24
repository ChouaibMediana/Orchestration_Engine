import pandas as pd
import requests
import json

print("🚀 Lancement du test de prédiction en masse (Batch Prediction)...")

# 1. On charge le fichier CSV avec Pandas
csv_file = "patients_test.csv"
try:
    df = pd.read_csv(csv_file)
    print(f"📊 Fichier CSV chargé avec succès : {len(df)} patients trouvés.")
except FileNotFoundError:
    print(f"❌ Erreur : Le fichier {csv_file} est introuvable.")
    exit()

# 2. On transforme le DataFrame (tableau) en une liste de dictionnaires
# Le format 'records' donne exactement ce que notre API attend : [{"f0": 17.99...}, {"f0": 20.57...}]
donnees_json = df.to_dict(orient="records")

# 3. On emballe ça dans la structure attendue par l'API
payload = {
    "data": donnees_json
}

# 4. On envoie tout au serveur Docker / Uvicorn
url = "http://localhost:8000/predict"
print(f"📦 Envoi de {len(donnees_json)} requêtes à l'API...")

try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        resultat = response.json()
        predictions = resultat["predictions"]
        
        print("\n" + "="*50)
        print("✅ SUCCÈS : L'API a traité le fichier CSV !")
        
        # On affiche les résultats de manière élégante
        for index, pred in enumerate(predictions):
            print(f"  🧑‍⚕️ Patient n°{index + 1} -> Prédiction : Classe {pred}")
        print("="*50 + "\n")
        
    else:
        print(f"❌ Erreur de l'API (Code {response.status_code}) : {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Impossible de se connecter. Es-tu sûr que ton serveur est allumé ?")