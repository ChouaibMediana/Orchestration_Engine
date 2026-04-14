import logging
from typing import List

from core.base import MLModule

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class PipelineOrchestrator:

    def __init__(self):
        self._stages: List[MLModule] = []  # Liste ordonnée des modules

    def register(self, module: MLModule) -> bool:
      if not isinstance(module, MLModule):
        return False
      self._stages.append(module)
      logger.info(f"Module enregistré : {module.__class__.__name__}")
      return True
    
    
    def run_pipeline(self) -> bool:
       
        logger.info(f"Démarrage du pipeline ({len(self._stages)} étapes)")

        for stage in self._stages:
            name = stage.__class__.__name__
            logger.info(f"--- Démarrage : {name} ---")

            try:
                stage.load()

                if not stage.validate():
                    raise ValueError(f"Validation échouée pour {name}")

                stage.run()
                logger.info(f"--- Terminé : {name} ---")

            except Exception as e:
                logger.error(f"ERREUR dans {name} : {e}")
                return False  # Fail-fast : on arrête tout

        logger.info("Pipeline terminé avec succès.")
        return True