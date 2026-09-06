"""EN: Domain interfaces defining contracts for evaluators and persistence repositories. | ES: Interfaces de dominio que definen contratos para evaluadores y repositorios de persistencia."""

from abc import ABC, abstractmethod

from domain.entities import (
    EthicalAssessment,
    FrameworkAssessment,
    FrameworkType,
    Scenario,
)


class IEthicalEvaluator(ABC):
    """EN: Interface contract for ethical framework evaluators. | ES: Contrato de interfaz para evaluadores de marcos eticos."""

    @property
    @abstractmethod
    def framework(self) -> FrameworkType:
        """EN: Return the framework type evaluated by this engine. | ES: Retorna el tipo de marco evaluado por este motor."""
        pass

    @abstractmethod
    def evaluate(self, scenario: Scenario) -> FrameworkAssessment:
        """EN: Evaluate a computational linguistics scenario against this framework. | ES: Evalua un escenario de linguistica computacional frente a este marco."""
        pass


class IScenarioRepository(ABC):
    """EN: Interface contract for scenario storage and retrieval. | ES: Contrato de interfaz para el almacenamiento y recuperacion de escenarios."""

    @abstractmethod
    def get_by_id(self, scenario_id: str) -> Scenario | None:
        """EN: Retrieve scenario by its unique identifier. | ES: Recuperar escenario por su identificador unico."""
        pass

    @abstractmethod
    def list_all(self) -> list[Scenario]:
        """EN: List all available evaluation scenarios. | ES: Listar todos los escenarios de evaluacion disponibles."""
        pass

    @abstractmethod
    def save(self, scenario: Scenario) -> None:
        """EN: Persist a new or modified scenario entity. | ES: Persistir una entidad de escenario nueva o modificada."""
        pass


class IAssessmentRepository(ABC):
    """EN: Interface contract for assessment persistence. | ES: Contrato de interfaz para la persistencia de evaluaciones."""

    @abstractmethod
    def save(self, assessment: EthicalAssessment) -> None:
        """EN: Persist an ethical assessment aggregate. | ES: Persistir un agregado de evaluacion etica."""
        pass

    @abstractmethod
    def get_by_id(self, assessment_id: str) -> EthicalAssessment | None:
        """EN: Retrieve an assessment by its unique identifier. | ES: Recuperar una evaluacion por su identificador unico."""
        pass

    @abstractmethod
    def list_by_scenario(self, scenario_id: str) -> list[EthicalAssessment]:
        """EN: List past assessments for a given scenario. | ES: Listar evaluaciones previas para un escenario dado."""
        pass
