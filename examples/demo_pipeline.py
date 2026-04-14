from core.base import MLModule
from core.decorators import track_state
from core.orchestrator import PipelineOrchestrator


# --- Modules fictifs ---

class DataIngestion(MLModule):
    def __init__(self):
        self._state = "IDLE"
        self._error = None

    def load(self):
        print("  [DataIngestion] Chargement des données...")

    @track_state
    def run(self):
        print("  [DataIngestion] Ingestion en cours...")

    def validate(self) -> bool:
        print("  [DataIngestion] Validation OK")
        return True

    def get_status(self) -> str:
        return self._state


class ModelTraining(MLModule):
    def __init__(self):
        self._state = "IDLE"
        self._error = None

    def load(self):
        print("  [ModelTraining] Chargement du modèle...")

    @track_state
    def run(self):
        print("  [ModelTraining] Entraînement en cours...")

    def validate(self) -> bool:
        print("  [ModelTraining] Validation OK")
        return True

    def get_status(self) -> str:
        return self._state


class ModelServing(MLModule):
    def __init__(self):
        self._state = "IDLE"
        self._error = None

    def load(self):
        print("  [ModelServing] Chargement du serving...")

    @track_state
    def run(self):
        print("  [ModelServing] Déploiement en cours...")

    def validate(self) -> bool:
        print("  [ModelServing] Validation OK")
        return True

    def get_status(self) -> str:
        return self._state


# --- Lancement du pipeline ---

if __name__ == "__main__":
    orchestrator = PipelineOrchestrator()

    orchestrator.register(DataIngestion())
    orchestrator.register(ModelTraining())
    orchestrator.register(ModelServing())

    success = orchestrator.run_pipeline()
    print(f"\nRésultat final : {'✅ Succès' if success else '❌ Échec'}")