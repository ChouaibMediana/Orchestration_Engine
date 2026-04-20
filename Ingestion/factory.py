# Importation de tes différentes classes
from .api_connector import APIConnector
from .db_connector import DBConnector
from .csv_connector import CSVConnector

def get_ingestion_connector(source_type, **kwargs):
    """
    La Factory : retourne la bonne instance de MLModule selon le type de source.
    """
    
    if source_type == "api":
        return APIConnector(
            endpoint=kwargs.get("url"), 
            params=kwargs.get("params"),
            headers=kwargs.get("headers")) # <-- Ajout ici
    
    elif source_type == "db":
        return DBConnector(
            connection_string=kwargs.get("conn_str"), 
            query=kwargs.get("query")
        )
        
    elif source_type == "csv":
        return CSVConnector(file_path=kwargs.get("path"))
        
    else:
        raise ValueError(f"Type de source '{source_type}' non reconnu par la Factory.")