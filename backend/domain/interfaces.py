"""EN: Domain interfaces defining contracts for evaluators and persistence repositories. | ES: Interfaces de dominio que definen contratos para evaluadores y repositorios de persistencia."""

from abc import ABC, abstractmethod

from domain.entities import (
    CaseStudy,
    DecisionImpactResult,
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


class ICaseStudyRepository(ABC):
    """EN: Interface contract for case study storage and retrieval. | ES: Contrato de interfaz para el almacenamiento y recuperacion de casos de estudio."""

    @abstractmethod
    def get_by_id(self, case_id: str) -> CaseStudy | None:
        """EN: Retrieve case study by its unique identifier. | ES: Recuperar caso de estudio por su identificador unico."""
        pass

    @abstractmethod
    def list_all(self) -> list[CaseStudy]:
        """EN: List all available computational linguistics case studies. | ES: Listar todos los casos de estudio de linguistica computacional disponibles."""
        pass

    @abstractmethod
    def save(self, case_study: CaseStudy) -> None:
        """EN: Persist a case study entity. | ES: Persistir una entidad de caso de estudio."""
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


class IDecisionImpactRepository(ABC):
    """EN: Interface contract for decision impact result persistence. | ES: Contrato de interfaz para la persistencia del resultado del impacto de la decision."""

    @abstractmethod
    def save(self, result: DecisionImpactResult) -> None:
        """EN: Persist a decision impact calculation result. | ES: Persistir el resultado de un calculo de impacto de decision."""
        pass

    @abstractmethod
    def get_by_id(self, decision_id: str) -> DecisionImpactResult | None:
        """EN: Retrieve a decision impact result by decision ID. | ES: Recuperar el resultado de un impacto de decision por ID de decision."""
        pass

    @abstractmethod
    def list_by_case(self, case_id: str) -> list[DecisionImpactResult]:
        """EN: List all past decision impact results for a case study. | ES: Listar todos los resultados previos de impacto de decision para un caso de estudio."""
        pass
