# 1. Image de base officielle Python (version allégée)
FROM python:3.12-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances en premier
COPY requirements.txt .

# 4. Installer les dépendances (avec ton correctif NumPy et Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "numpy<2" uvicorn

# 5. Copier tout le reste du code (y compris best_model.joblib et le dossier serving)
COPY . .

# 6. Indiquer le port sur lequel l'API va écouter
EXPOSE 8000

# 7. La commande pour lancer ton API au démarrage du conteneur
CMD ["uvicorn", "serving.api:app", "--host", "0.0.0.0", "--port", "8000"]
