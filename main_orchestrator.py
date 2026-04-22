import asyncio
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

from core.orchestrator import PipelineOrchestrator
from training.trainer import Trainer
from serving.deployment import FastAPIServingModule

async def main():
    # 1. Préparation des données (Simulation Ingestion)
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 2. Configuration du module de Rida (Training)
    trainer_module = Trainer(
        model_class=RandomForestClassifier,
        param_grid={'n_estimators': [50, 100], 'max_depth': [None, 5]},
        X_train=X,
        y_train=y
    )

    # 3. Configuration de ton module (Serving)
    serving_module = FastAPIServingModule(port=8000)

    # 4. Orchestration
    orchestrator = PipelineOrchestrator()
    orchestrator.register(trainer_module)
    orchestrator.register(serving_module)

    print("\n⚡ Lancement du Pipeline MLOps Complet...")
    await orchestrator.run_pipeline()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du pipeline.")