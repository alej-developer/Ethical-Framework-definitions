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
