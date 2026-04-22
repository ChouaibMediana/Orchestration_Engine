from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import joblib
import pandas as pd
import os

app = FastAPI(title="MLOps Dynamic Orchestrator API", description="API générique pour modèles ML")

model = None

# On accepte un dictionnaire dynamique (ex: {"age": 25, "salaire": 3000})
class DynamicPredictionRequest(BaseModel):
    data: List[Dict[str, Any]]

@app.on_event("startup")
def load_model():
    global model
    model_path = "best_model.joblib"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("✅ API : Modèle générique chargé avec succès.")

@app.post("/predict")
def predict(request: DynamicPredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Aucun modèle entraîné n'a été trouvé.")
    
    try:
        # On transforme la liste de dictionnaires en DataFrame Pandas (format standard scikit-learn)
        # Cela gérera automatiquement les noms des colonnes !
        input_data = pd.DataFrame(request.data)
        
        # On effectue la prédiction
        predictions = model.predict(input_data)
        
        # On retourne les résultats
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction (Vérifiez les colonnes) : {str(e)}")