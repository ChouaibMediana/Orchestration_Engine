# 🤖 ML Pipeline Orchestrator

> Framework Python modulaire pour automatiser le cycle de vie complet d'un projet Machine Learning.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)
![pytest](https://img.shields.io/badge/Tests-pytest-yellow?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/Licence-MIT-green)
![Status](https://img.shields.io/badge/Statut-En%20développement-orange)

---

## 📌 Présentation

**ML Pipeline Orchestrator** est un framework Python conçu pour orchestrer automatiquement chaque étape du cycle de vie d'un modèle Machine Learning :

- 📥 **Ingestion** — Connexion multi-sources et validation des données entrantes
- ⚙️ **Preprocessing** — Pipeline de transformation modulaire et interchangeable
- 🧠 **Entraînement** — Training concurrent avec gestion asynchrone et tuning d'hyperparamètres
- 🚀 **Déploiement** — Serving en production via FastAPI avec registre de modèles

Le projet repose sur une architecture extensible à base de **classes abstraites (ABC)**, de **décorateurs de tracking d'état**, et d'un moteur d'orchestration **fail-fast** pensé pour le travail en équipe.

---

## 🏗️ Architecture du projet

```
ml_pipeline_orchestrator/
├── core/
│   ├── __init__.py
│   ├── base.py            # Classe abstraite MLModule (contrat commun)
│   ├── orchestrator.py    # Moteur d'orchestration séquentiel
│   └── decorators.py      # Décorateurs de tracking d'état et de temps
├── ingestion/
│   └── factory.py         # Connecteurs multi-sources (API, CSV, DB)
├── training/
│   └── trainer.py         # Entraînement async + tuning hyperparamètres
├── serving/
│   └── api.py             # Endpoints FastAPI + registre de modèles
├── tests/
│   └── test_orchestrator.py
├── examples/
│   └── demo_pipeline.py
└── README.md
```

---

## ⚙️ Piliers techniques

| Pilier | Description | Technologies |
|---|---|---|
| **Modularisation** | Chaque étape est un module interchangeable via ABCs | `abc`, `typing` |
| **Concurrence** | Entraînement parallèle et inférence asynchrone | `asyncio`, `ThreadPoolExecutor` |
| **Ingestion** | Connecteurs automatisés vers sources multiples | `pandas`, API Wrappers |
| **Déploiement** | Serving production containerisé | `FastAPI`, `Docker` |

---

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/ton-username/ml-pipeline-orchestrator.git
cd ml-pipeline-orchestrator

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## 🧪 Utilisation rapide

```python
from core.orchestrator import PipelineOrchestrator
from core.base import MLModule
from core.decorators import track_state

# Créer un module personnalisé
class MonModule(MLModule):
    def __init__(self):
        self._state = "IDLE"

    def load(self): 
        print("Chargement...")

    @track_state
    def run(self): 
        print("Exécution...")

    def validate(self) -> bool: 
        return True

    def get_status(self) -> str: 
        return self._state

# Construire et lancer le pipeline
pipeline = PipelineOrchestrator()
pipeline.register(MonModule())
pipeline.run_pipeline()
```

---

## 🧪 Lancer les tests

```bash
pytest tests/ -v
```

---
## 🐳 Déploiement et Inférence (API & Docker)

La couche de déploiement (Serving) expose le modèle entraîné via une API REST dynamique et conteneurisée. L'API s'adapte automatiquement aux variables du modèle grâce à une architecture de requêtes génériques.

### Lancer l'API avec Docker (Recommandé)
Assurez-vous que Docker est installé sur votre machine, puis exécutez ces commandes à la racine du projet :

1. **Construire l'image :**
   ```bash
   docker build -t mlops-api:v1 .

    Démarrer le conteneur :
    Bash

    docker run -p 8000:8000 mlops-api:v1

Tester les prédictions

Une fois le serveur en ligne, une interface interactive Swagger est générée automatiquement.
👉 Accédez à : http://localhost:8000/docs

Vous pouvez tester la route POST /predict en envoyant vos données sous ce format dynamique (ajustez les clés selon le dataset d'entraînement) :
JSON

{
  "data": [
    {
      "feature_0": 17.99,
      "feature_1": 10.38,
      "feature_2": 122.8
    }
  ]
}

---

## 🗓️ Roadmap — 4 semaines

| Semaine | Objectif | Responsable |
|---|---|---|
| Semaine 1 | Core Orchestrator & structure OOP | Chouaib Mediana |
| Semaine 2 | Data Connectors & preprocessing modulaire | Anass Moulim |
| Semaine 3 | Async Training & tuning | Rida Mellouki |
| Semaine 4 | FastAPI Serving & intégration finale | Ziad Lachguer |

---

## 👥 Équipe

| Nom | Rôle | Module |
|---|---|---|
| **Chouaib Mediana** | Framework Architecture | Orchestration Engine |
| **Rida Mellouki** | System Performance | Concurrency & Tuning |
| **Anass Moulim** | Data Engineering | Ingestion Factory |
| **Ziad Lachguer** | MLOps Infrastructure | Deployment Layer |

---

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).
