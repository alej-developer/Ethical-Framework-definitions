"""EN: Centralized exception handling middleware producing standardized JSON error envelopes. | ES: Middleware centralizado de manejo de excepciones que genera envoltorios de error JSON estandarizados."""

from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from domain.exceptions import (
    CaseStudyNotFoundError,
    DomainError,
    InvalidDecisionOptionError,
    ScenarioNotFoundError,
    UnsupportedFrameworkError,
)


def _build_error_payload(
    code: str,
    message: str,
    status_code: int,
    details: Any = None,
) -> dict[str, Any]:
    """EN: Construct standard dictionary for error response envelope. | ES: Construir diccionario estandar para envoltorio de respuesta de error."""
    return {
        "error": {
            "code": code,
            "message": message,
            "status_code": status_code,
            "details": details,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    }


def register_error_handlers(app: FastAPI) -> None:
    """EN: Register centralized exception handlers on the FastAPI application instance. | ES: Registrar manejadores centralizados de excepciones en la instancia de aplicacion FastAPI."""

    @app.exception_handler(CaseStudyNotFoundError)
    async def handle_case_study_not_found(request: Request, exc: CaseStudyNotFoundError) -> JSONResponse:
        payload = _build_error_payload(
            code="CASE_STUDY_NOT_FOUND",
            message=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
            details={"case_id": exc.case_id},
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload)

    @app.exception_handler(ScenarioNotFoundError)
    async def handle_scenario_not_found(request: Request, exc: ScenarioNotFoundError) -> JSONResponse:
        payload = _build_error_payload(
            code="SCENARIO_NOT_FOUND",
            message=str(exc),
            status_code=status.HTTP_404_NOT_FOUND,
            details={"scenario_id": exc.scenario_id},
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=payload)

    @app.exception_handler(InvalidDecisionOptionError)
    async def handle_invalid_decision_option(request: Request, exc: InvalidDecisionOptionError) -> JSONResponse:
        payload = _build_error_payload(
            code="INVALID_DECISION_OPTION",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"case_id": exc.case_id, "option_id": exc.option_id},
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload)

    @app.exception_handler(UnsupportedFrameworkError)
    async def handle_unsupported_framework(request: Request, exc: UnsupportedFrameworkError) -> JSONResponse:
        payload = _build_error_payload(
            code="UNSUPPORTED_FRAMEWORK",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"framework_name": exc.framework_name},
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload)

    @app.exception_handler(DomainError)
    async def handle_generic_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        payload = _build_error_payload(
            code="DOMAIN_ERROR",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=payload)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        formatted_errors = [
            {
                "field": ".".join(str(loc) for loc in err.get("loc", [])),
                "issue": err.get("msg", "Validation error"),
                "type": err.get("type", "value_error"),
            }
            for err in exc.errors()
        ]
        payload = _build_error_payload(
            code="VALIDATION_ERROR",
            message="Request body or query parameters failed schema validation.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=formatted_errors,
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload)

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        payload = _build_error_payload(
            code="HTTP_ERROR",
            message=str(exc.detail),
            status_code=exc.status_code,
        )
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        payload = _build_error_payload(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal server error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"exception_type": type(exc).__name__},
        )
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)
