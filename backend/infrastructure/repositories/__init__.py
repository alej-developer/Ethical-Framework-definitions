"""EN: Repositories package initialization. | ES: Inicializacion del paquete de repositorios."""

from infrastructure.repositories.in_memory_repository import (
    InMemoryAssessmentRepository,
    InMemoryScenarioRepository,
)

__all__ = ["InMemoryAssessmentRepository", "InMemoryScenarioRepository"]
