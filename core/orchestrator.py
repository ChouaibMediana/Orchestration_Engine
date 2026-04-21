import logging
import asyncio
from typing import List
from concurrent.futures import ProcessPoolExecutor
from core.base import MLModule

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class PipelineOrchestrator:

    def __init__(self, max_workers: int = 4):
        #Mellouki Modif
        self._stages: List[MLModule] = []
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def register(self, module: MLModule) -> bool:
        if not isinstance(module, MLModule):
            return False
        self._stages.append(module)
        logger.info(f"Module enregistré : {module.__class__.__name__}")
        return True
    async def run_pipeline(self) -> bool:
        logger.info(f"Démarrage du pipeline ({len(self._stages)} étapes)")
        #mellouki MODIF i change that from sync to async function 
        loop = asyncio.get_running_loop()
        for stage in self._stages:
            name = stage.__class__.__name__
            logger.info(f"--- Démarrage : {name} ---")

            try:
                stage.load()
                if not stage.validate():
                    raise ValueError(f"Validation échouée pour {name}")
                # Check if the run method is async
                run_method = getattr(stage, "run")
                if asyncio.iscoroutinefunction(run_method) or asyncio.iscoroutinefunction(getattr(run_method, '__wrapped__', None)):
                    logger.info(f"--Awaiting {name} (Native Async Mode)")
                    await run_method()
                else:
                    stage.run()
                    
                logger.info(f"--- Terminé : {name} ---")
            except Exception as e:
                logger.error(f"ERREUR dans {name} : {e}")
                return False 

        logger.info("Pipeline terminé avec succès.")
        return True
    #for shutting down the executor (ProcessPoolExecutor) 
    def shutdown(self):
        self.executor.shutdown()