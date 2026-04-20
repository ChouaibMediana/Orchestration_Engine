from core.base import MLModule
from core.decorators import track_state
import pandas as pd
import requests

class APIConnector(MLModule):
    def __init__(self, endpoint, params=None, headers=None): # <-- Ajout de headers
        self.endpoint = endpoint
        self.params = params
        self.headers = headers # <-- Sauvegarde des headers
        self.data = None
        self._state = "IDLE"

    def load(self):
        try:
            # On passe les headers ici aussi pour le test de connexion
            response = requests.head(self.endpoint, headers=self.headers, timeout=5)
            if response.status_code == 200:
                print(f"Connexion réussie à {self.endpoint}")
            else:
                print(f"Alerte : Statut {response.status_code}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    @track_state
    def run(self):
        print(f"Récupération des données depuis {self.endpoint}...")
        # On ajoute les headers dans la requête GET
        response = requests.get(self.endpoint, params=self.params, headers=self.headers)
        
        if response.status_code == 200:
            json_data = response.json()
            self.data = pd.DataFrame(json_data)
            return self.data
        else:
            print(f"Détail de l'erreur : {response.text}") # Utile pour le debug
            raise Exception(f"Échec de l'ingestion : {response.status_code}")

    def validate(self) -> bool:
        """
        Vérifie si les données reçues ne sont pas vides[cite: 18].
        """
        if self.data is not None and not self.data.empty:
            print("Validation réussie : Données récupérées.")
            return True
        return False

    def get_status(self) -> str:
        """
        Retourne l'état actuel du module pour l'orchestrateur[cite: 19].
        """
        return self._state