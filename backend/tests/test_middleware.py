"""EN: Unit tests verifying centralized error handling middleware and standard error envelopes. | ES: Pruebas unitarias que verifican el middleware centralizado de manejo de errores y envoltorios de error estandar."""

from fastapi.testclient import TestClient

from infrastructure.main import app

client = TestClient(app)


def test_case_study_not_found_returns_standard_error() -> None:
    """EN: Verify 404 response follows standardized error envelope for missing case study. | ES: Verificar que la respuesta 404 siga el envoltorio de error estandarizado para caso de estudio faltante."""
    response = client.get("/api/v1/cases/non-existent-case-999")
    assert response.status_code == 404

    data = response.json()
    assert "error" in data
    error = data["error"]
    assert error["code"] == "CASE_STUDY_NOT_FOUND"
    assert error["status_code"] == 404
    assert "non-existent-case-999" in error["message"]
    assert error["details"]["case_id"] == "non-existent-case-999"
    assert "timestamp" in error


def test_scenario_not_found_returns_standard_error() -> None:
    """EN: Verify 404 response follows standardized error envelope for missing scenario. | ES: Verificar que la respuesta 404 siga el envoltorio de error estandarizado para escenario faltante."""
    response = client.get("/api/v1/scenarios/non-existent-scenario-999")
    assert response.status_code == 404

    data = response.json()
    assert "error" in data
    error = data["error"]
    assert error["code"] == "SCENARIO_NOT_FOUND"
    assert error["status_code"] == 404


def test_invalid_decision_option_returns_standard_error() -> None:
    """EN: Verify submitting an invalid option returns 400 with INVALID_DECISION_OPTION. | ES: Verificar que enviar una opcion invalida retorne 400 con INVALID_DECISION_OPTION."""
    payload = {
        "case_id": "cs-recruitment-llm-001",
        "selected_option_id": "invalid-option-xyz",
        "user_rationale": "Sufficiently long rationale explaining my selection.",
    }
    response = client.post("/api/v1/decisions", json=payload)
    assert response.status_code == 400

    data = response.json()
    assert "error" in data
    error = data["error"]
    assert error["code"] == "INVALID_DECISION_OPTION"
    assert error["status_code"] == 400
    assert error["details"]["option_id"] == "invalid-option-xyz"


def test_validation_error_returns_standard_error() -> None:
    """EN: Verify Pydantic V2 validation failure returns 422 with structured details. | ES: Verificar que el fallo de validacion de Pydantic V2 retorne 422 con detalles estructurados."""
    # EN: user_rationale is too short (< 10 chars) | ES: user_rationale es demasiado corto (< 10 caracteres)
    payload = {
        "case_id": "cs-recruitment-llm-001",
        "selected_option_id": "opt-recruit-status-quo",
        "user_rationale": "Short",
    }
    response = client.post("/api/v1/decisions", json=payload)
    assert response.status_code == 422

    data = response.json()
    assert "error" in data
    error = data["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["status_code"] == 422
    assert isinstance(error["details"], list)
    assert any("user_rationale" in d.get("field", "") for d in error["details"])
