import time
import tracemalloc
import asyncio
from functools import wraps

def track_state(method):
    """Décorateur qui suit l'état et le temps d'exécution d'une méthode.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # --- Avant l'exécution ---
        self._state = "RUNNING"
        tracemalloc.start()
        start = time.perf_counter()  # used for high-resolution performance measurement
        name = self.__class__.__name__
        print(f"  → [{name}] État : RUNNING")
        try:
            # --- Exécution de la méthode originale ---
            result = method(self, *args, **kwargs)
            current , peak = tracemalloc.get_traced_memory() #  Return (current, peak) memory usage in bytes
            tracemalloc.stop()
            # --- Succès ---
            self._state = "DONE"
            elapsed = time.perf_counter() - start
            print(f"  ✓ [{name}] État : DONE ({elapsed:.2f}s)")
            return result

        except Exception as e:
            # --- Échec ---
            self._state = "ERROR"
            self._error = str(e)
            print(f"  ✗ [{name}] État : ERROR — {e}")
            raise  # re-lève pour que l'orchestrateur la reçoive
    @wraps(method)
    async def async_wrapper(self, *args, **kwargs):
        # --- Avant l'exécution ---
        tracemalloc.start()
        start = time.perf_counter()  # used for high-resolution performance measurement
        name = self.__class__.__name__
        print(f"  → [{name}] État : RUNNING")

        try:
            # --- Exécution de la méthode originale ---
            result = await method(self, *args, **kwargs)

            # --- Succès ---
            self._state = "DONE"
            elapsed = time.perf_counter() - start
            print(f"  ✓ [{name}] État : DONE ({elapsed:.2f}s)")
            return result

        except Exception as e:
            # --- Échec ---
            self._state = "ERROR"
            self._error = str(e)
            print(f"  ✗ [{name}] État : ERROR — {e}")
            raise  # re-lève pour que l'orchestrateur la reçoive

    return async_wrapper if asyncio.iscoroutinefunction(method) else wrapper