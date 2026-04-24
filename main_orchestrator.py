import argparse
import pandas as pd
import asyncio
import os
from sklearn.ensemble import RandomForestClassifier

from core.orchestrator import PipelineOrchestrator
from training.trainer import Trainer

def main():
    # 1. Définition des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Moteur d'Orchestration MLOps Universel")
    parser.add_argument("--data", type=str, required=True, help="Chemin vers le fichier CSV de données")
    parser.add_argument("--target", type=str, required=True, help="Nom de la colonne cible (Y) à prédire")
    
    # Récupération des arguments tapés par l'utilisateur
    args = parser.parse_args()

    print("\n" + "="*50)
    print(f"📂 Pipeline initialisé avec le dataset : {args.data}")
    print(f"🎯 Variable cible (Target) : {args.target}")
    print("="*50 + "\n")

    # 2. Chargement dynamique et agnostique des données
    try:
        df = pd.read_csv(args.data)
        # Séparation de X (les features) et y (la cible)
        y = df[args.target].values
        X = df.drop(columns=[args.target]).values
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{args.data}' est introuvable.")
        return
    except KeyError:
        print(f"❌ Erreur : La colonne cible '{args.target}' n'existe pas dans le CSV.")
        return

    # 3. Configuration de la grille de recherche (Hyperparamètres)
    param_grid = {
        'n_estimators': [10, 50, 100],
        'max_depth': [2, 5, None]
    }

    # 4. Instanciation des modules MLOps
    orchestrator = PipelineOrchestrator(max_workers=4)
    
    # On passe le X et y générés dynamiquement
    trainer = Trainer(RandomForestClassifier, param_grid, X, y)
    
    # Enregistrement de l'étape
    orchestrator.register(trainer)

    # 5. Exécution asynchrone du pipeline
    try:
        success = asyncio.run(orchestrator.run_pipeline())
        if success:
            print("\n✅ Entraînement terminé avec succès ! Modèle sauvegardé.")
    finally:
        # Assure la fermeture propre du ProcessPoolExecutor
        orchestrator.shutdown()

if __name__ == "__main__":
    main()