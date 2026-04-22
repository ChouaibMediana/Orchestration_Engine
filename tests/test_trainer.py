import pytest
import asyncio
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from training.trainer import Trainer

@pytest.fixture
def dummy_data():
    """Crée un petit jeu de données pour les tests."""
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    return X, y

def test_trainer_load(dummy_data):
    """Vérifie que la méthode load sépare bien les données."""
    X, y = dummy_data
    param_grid = {'n_estimators': [10]}
    trainer = Trainer(RandomForestClassifier, param_grid, X, y)
    
    trainer.load()
    
    # Assert data split happened (80% train, 20% validation)
    assert hasattr(trainer, 'X_t')
    assert hasattr(trainer, 'X_validation')
    assert trainer.X_t.shape[0] == 80
    assert trainer.X_validation.shape[0] == 20

def test_trainer_validate_logic(dummy_data):
    """Vérifie que validate() exige que load() soit exécuté en premier."""
    X, y = dummy_data
    param_grid = {'n_estimators': [10]}
    trainer = Trainer(RandomForestClassifier, param_grid, X, y)
    
    # Avant load(), hasattr(self, 'X_t') est False
    assert not trainer.validate()
    
    trainer.load()
    # Après load(), hasattr(self, 'X_t') est True
    assert trainer.validate()

def test_trainer_async_run_and_state(dummy_data):
    """Vérifie que run() entraîne les modèles en parallèle et que le décorateur met à jour l'état."""
    X, y = dummy_data
    param_grid = {'n_estimators': [5, 10], 'max_depth': [2, 5]}
    trainer = Trainer(RandomForestClassifier, param_grid, X, y)
    
    assert trainer.get_status() == "IDLE"
    
    trainer.load()
    
    # On exécute la méthode asynchrone run()
    best_model = asyncio.run(trainer.run())
    
    # 1. Vérifie que le meilleur modèle a été trouvé
    assert best_model is not None
    assert trainer.best_model is not None
    assert trainer.best_score > 0
    assert len(trainer.results) == 4  # 2 n_estimators * 2 max_depth = 4 configs
    
    # 2. Vérifie que le décorateur a bien défini l'état à DONE
    assert trainer.get_status() == "DONE"
