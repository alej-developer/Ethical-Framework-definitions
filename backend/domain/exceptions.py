"""EN: Domain exceptions for the AI ethics evaluation engine. | ES: Excepciones de dominio para el motor de evaluacion de etica en IA."""


class DomainError(Exception):
    """EN: Base domain exception. | ES: Excepcion base de dominio."""

    pass


class ScenarioNotFoundError(DomainError):
    """EN: Raised when a requested evaluation scenario is not found. | ES: Se lanza cuando no se encuentra un escenario de evaluacion solicitado."""

    def __init__(self, scenario_id: str) -> None:
        # EN: Initialize error with missing identifier | ES: Inicializar error con identificador faltante
        self.scenario_id = scenario_id
        super().__init__(f"Scenario with id '{scenario_id}' was not found.")


class CaseStudyNotFoundError(DomainError):
    """EN: Raised when a requested case study is not found. | ES: Se lanza cuando no se encuentra un caso de estudio solicitado."""

    def __init__(self, case_id: str) -> None:
        # EN: Initialize error with missing case identifier | ES: Inicializar error con identificador de caso faltante
        self.case_id = case_id
        super().__init__(f"Case study with id '{case_id}' was not found.")


class InvalidDecisionOptionError(DomainError):
    """EN: Raised when an invalid or nonexistent decision option is submitted. | ES: Se lanza cuando se envia una opcion de decision invalida o inexistente."""

    def __init__(self, case_id: str, option_id: str) -> None:
        # EN: Initialize error with invalid option details | ES: Inicializar error con detalles de opcion invalida
        self.case_id = case_id
        self.option_id = option_id
        super().__init__(f"Option '{option_id}' is invalid for case study '{case_id}'.")


class InvalidMetricValueError(DomainError):
    """EN: Raised when a calculated or provided metric is outside valid bounds. | ES: Se lanza cuando una metrica calculada o provista esta fuera de los limites validos."""

    def __init__(self, metric_name: str, value: float) -> None:
        # EN: Initialize error with invalid metric details | ES: Inicializar error con detalles de la metrica invalida
        self.metric_name = metric_name
        self.value = value
        super().__init__(f"Metric '{metric_name}' value {value} is out of valid bounds.")


class UnsupportedFrameworkError(DomainError):
    """EN: Raised when an evaluation is requested for an unsupported framework. | ES: Se lanza cuando se solicita una evaluacion para un marco no soportado."""

    def __init__(self, framework_name: str) -> None:
        # EN: Initialize error with unsupported framework name | ES: Inicializar error con nombre de marco no soportado
        self.framework_name = framework_name
        super().__init__(f"Framework '{framework_name}' is not supported.")
