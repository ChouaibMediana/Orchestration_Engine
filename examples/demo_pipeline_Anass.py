from core.orchestrator import PipelineOrchestrator
# On importe la Factory depuis ton module
from Ingestion.factory import get_ingestion_connector 

# 1. On demande un connecteur à la Factory
api_module = get_ingestion_connector(
    source_type="api", 
    url="https://jsonplaceholder.typicode.com/users"
)

# 2. On l'enregistre dans le pipeline
pipeline = PipelineOrchestrator()
pipeline.register(api_module)
pipeline.run_pipeline()