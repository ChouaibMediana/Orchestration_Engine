import asyncio
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

from core.orchestrator import PipelineOrchestrator
from training.trainer import Trainer

async def main():
    print("🚀 Démarrage du test Concurrency & Tuning...")
    
    data = load_breast_cancer()
    X = data.data
    y = data.target
    
    print(f"📦 Données chargées : {X.shape[0]} lignes, {X.shape[1]} features.")

    # 2. Define the Hyperparameters Grid for RandomForest
    param_grid = {
        'n_estimators': [10, 50, 100],
        'max_depth': [None, 5, 10],
        'min_samples_split': [2, 5]
    }
    
    print("⚙️ Paramètres à tester (Hyperparameter Grid) :")
    print(param_grid)

    # 3. Initialize the Trainer (from training.trainer)
    trainer_module = Trainer(
        model_class=RandomForestClassifier,
        param_grid=param_grid,
        X_train=X,
        y_train=y,
        max_workers=4
    )

    # 4. Initialize the Orchestrator and Register the Trainer
    orchestrator = PipelineOrchestrator(max_workers=4)
    orchestrator.register(trainer_module)

    # 5. Run the Engine!
    print("\n⚡ Lancement de l'Orchestrateur (Async / ProcessPool) :")
    success = await orchestrator.run_pipeline()
    
    # 6. Clean up
    orchestrator.shutdown()
    
    print(f"\n🎯 Résultat de l'Orchestrateur : {'Succès' if success else 'Échec'}")

if __name__ == "__main__":
    asyncio.run(main())
