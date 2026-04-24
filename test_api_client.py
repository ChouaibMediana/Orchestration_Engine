import requests
import json

print("🌐 Démarrage du test d'API MLOps...")

# L'URL de ton API locale (assure-toi qu'elle tourne !)
url = "http://localhost:8000/predict"

# On crée des données de test aléatoires (ici, 30 variables fictives pour simuler un patient)
import random
donnees_fictives = {f"feature_{i}": random.uniform(0.1, 150.0) for i in range(30)}

# Le format JSON dynamique que ton API attend
payload = {
    "data": [donnees_fictives]
}

print(f"📦 Envoi de la requête à {url}...")

try:
    # On envoie la requête POST à ton API
    response = requests.post(url, json=payload)
    
    # On vérifie si l'API a bien répondu (Code 200)
    if response.status_code == 200:
        resultat = response.json()
        print("\n" + "="*50)
        print("✅ SUCCÈS : L'API a répondu !")
        print(f"🎯 PRÉDICTION DU MODÈLE : {resultat['predictions'][0]}")
        print("="*50 + "\n")
    else:
        print(f"❌ Erreur de l'API (Code {response.status_code}) : {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Impossible de se connecter. Es-tu sûr que ton serveur FastAPI (ou Docker) est allumé ?")