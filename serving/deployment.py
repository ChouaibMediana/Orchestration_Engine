from core.base import MLModule
from core.decorators import track_state
import subprocess
import os
import time
import requests

class FastAPIServingModule(MLModule):
    def __init__(self, model_path: str = "best_model.joblib", port: int = 8000):
        self._state = "IDLE"
        self.model_path = model_path
        self.port = port
        self.server_process = None

    def load(self):
        print(f"🚀 Préparation du déploiement (Port: {self.port})...")

    def validate(self) -> bool:
        # On vérifie si Rida a bien généré le fichier modèle
        if not os.path.exists(self.model_path):
            print(f"❌ Erreur : Le fichier {self.model_path} est introuvable.")
            return False
        return True

    @track_state
    def run(self):
        self._state = "RUNNING"
        print(f"🌐 Lancement du serveur Uvicorn sur http://0.0.0.0:{self.port}")
        
        # On lance l'API dans un processus séparé pour ne pas bloquer l'orchestrateur
        self.server_process = subprocess.Popen(
            ["uvicorn", "serving.api:app", "--host", "0.0.0.0", "--port", str(self.port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # On attend quelques secondes que le serveur démarre
        time.sleep(3)
        print("✅ API en ligne et prête à recevoir des prédictions.")

    def get_status(self) -> str:
        return self._state