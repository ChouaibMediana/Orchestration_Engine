from core.base import MLModule
from core.decorators import track_state
import pandas as pd
from sqlalchemy import create_engine

class DBConnector(MLModule):
    def __init__(self, connection_string, query):
        """
        Initialise le connecteur avec la chaîne de connexion (URL) et la requête SQL.
        """
        self.connection_string = connection_string
        self.query = query
        self.engine = None
        self.data = None
        self._state = "IDLE"

    def load(self):
        """
        Crée le moteur de connexion à la base de données.
        """
        try:
            self.engine = create_engine(self.connection_string)
            # Test de connexion rapide
            with self.engine.connect() as conn:
                pass
            print("Connexion à la base de données établie.")
        except Exception as e:
            print(f"Erreur lors de la création du moteur DB : {e}")
            raise

    @track_state
    def run(self):
        """
        Exécute la requête SQL et charge les données dans un DataFrame.
        """
        if not self.engine:
            raise Exception("L'engine n'est pas chargé. Appelez load() d'abord.")
        
        print(f"Exécution de la requête : {self.query}")
        self.data = pd.read_sql(self.query, self.engine)
        return self.data

    def validate(self) -> bool:
        """
        Vérifie si les données extraites sont valides.
        """
        if self.data is not None and not self.data.empty:
            print(f"Validation réussie : {len(self.data)} lignes récupérées.")
            return True
        return False

    def get_status(self) -> str:
        """
        Retourne l'état actuel pour l'Orchestration Engine.
        """
        return self._state