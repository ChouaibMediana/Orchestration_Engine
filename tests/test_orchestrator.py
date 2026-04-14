import pytest
from core.base import MLModule
from core.orchestrator import PipelineOrchestrator


# Module fictif valide pour les tests
class FakeModule(MLModule):
    def __init__(self):
        self._state = "IDLE"
        self._error = None

    def load(self): pass
    def run(self): pass
    def validate(self) -> bool: return True
    def get_status(self) -> str: return self._state


# Module qui échoue volontairement
class FailingModule(MLModule):
    def __init__(self):
        self._state = "IDLE"
        self._error = None

    def load(self): pass
    def run(self): raise RuntimeError("Erreur simulée")
    def validate(self) -> bool: return True
    def get_status(self) -> str: return self._state


# Test 1 : register accepte un MLModule valide
def test_register_valid_module():
    orchestrator = PipelineOrchestrator()
    result = orchestrator.register(FakeModule())
    assert result == True
    assert len(orchestrator._stages) == 1


# Test 2 : register rejette un objet invalide
def test_register_invalid_module():
    orchestrator = PipelineOrchestrator()
    result = orchestrator.register("not_a_module")
    assert result == False
    assert len(orchestrator._stages) == 0


# Test 3 : pipeline s'arrête si un module échoue
def test_pipeline_stops_on_error():
    orchestrator = PipelineOrchestrator()
    orchestrator.register(FakeModule())
    orchestrator.register(FailingModule())
    result = orchestrator.run_pipeline()
    assert result == False


# Test 4 : pipeline retourne True si tout réussit
def test_pipeline_success():
    orchestrator = PipelineOrchestrator()
    orchestrator.register(FakeModule())
    orchestrator.register(FakeModule())
    result = orchestrator.run_pipeline()
    assert result == True