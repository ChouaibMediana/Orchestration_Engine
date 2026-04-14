from abc import ABC , abstractmethod


class MLModule(ABC):

    @abstractmethod
    def load(self) -> None:
        """charger les ressource rt les données depuit json ou xml csv etc ..."""
        pass
    
    @abstractmethod
    def run(self):
        """faire tout les étapes lire les donner train le modèle ,faire les prédictions et évaluer le modèle"""
        pass
    
    @abstractmethod
    def validate(self)-> bool:
        """verification les valeur null le mosule entrainé bien validation des resultat """
        pass
    
    @abstractmethod
    def get_status(self) -> str :
        """ status de l'execution du projet , si c'est en cours ou terminé ou échoué etc ..."""
        pass