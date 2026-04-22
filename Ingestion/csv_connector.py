from core.base import MLModule
from core.decorators import track_state
import pandas as pd

class CSVConnector(MLModule):
    def __init__(self, file_path):
        self.file_path = file_path
        self._state = "IDLE" 

    def load(self):
        # Logique pour vérifier si le fichier existe
        pass

    @track_state 
    def run(self):
        # Utilisation de pandas pour l'ingestion 
        self.data = pd.read_csv(self.file_path)
        return self.data

    def validate(self) -> bool:
        # Vérification si le DataFrame n'est pas vide
        return not self.data.empty 
    
    def get_status(self) -> str:
        """
        Retourne l'état actuel du module pour l'orchestrateur[cite: 19].
        """
        return self._state