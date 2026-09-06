"""EN: API integration tests validating FastAPI HTTP endpoints and error handling. | ES: Pruebas de integracion de API que validan los puntos finales HTTP de FastAPI y el manejo de errores."""

from fastapi.testclient import TestClient

from infrastructure.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """EN: Test GET /api/v1/health returns 200 and healthy status. | ES: Probar que GET /api/v1/health retorne 200 y estado saludable."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Clean Architecture" in data["architecture"]


def test_frameworks_endpoint() -> None:
    """EN: Test GET /api/v1/frameworks returns list of supported frameworks. | ES: Probar que GET /api/v1/frameworks retorne la lista de marcos soportados."""
    response = client.get("/api/v1/frameworks")
    assert response.status_code == 200
    frameworks = response.json()
    assert len(frameworks) == 2
    framework_ids = [f["id"] for f in frameworks]
    assert "EU_AI_ACT" in framework_ids
    assert "IEEE_7000_SERIES" in framework_ids


def test_list_scenarios_endpoint() -> None:
    """EN: Test GET /api/v1/scenarios retrieves seeded benchmark scenarios. | ES: Probar que GET /api/v1/scenarios recupere los escenarios de referencia inicializados."""
    response = client.get("/api/v1/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) >= 3
    ids = [s["id"] for s in scenarios]
    assert "nlp-dialect-bias-001" in ids
    assert "nlp-clinical-triage-002" in ids
    assert "nlp-translation-toxic-003" in ids


def test_get_single_scenario_success() -> None:
    """EN: Test GET /api/v1/scenarios/{id} returns scenario detail. | ES: Probar que GET /api/v1/scenarios/{id} retorne el detalle del escenario."""
    response = client.get("/api/v1/scenarios/nlp-dialect-bias-001")
    assert response.status_code == 200
    scenario = response.json()
    assert scenario["id"] == "nlp-dialect-bias-001"
    assert len(scenario["artifacts"]) > 0


def test_get_single_scenario_not_found() -> None:
    """EN: Test GET /api/v1/scenarios/{id} returns 404 for unknown scenario ID. | ES: Probar que GET /api/v1/scenarios/{id} retorne 404 para un ID de escenario desconocido."""
    response = client.get("/api/v1/scenarios/unknown-scenario-999")
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data


def test_evaluate_scenario_success() -> None:
    """EN: Test POST /api/v1/evaluations executes assessment and returns 201. | ES: Probar que POST /api/v1/evaluations ejecute la evaluacion y retorne 201."""
    payload = {
        "scenario_id": "nlp-clinical-triage-002",
        "frameworks": ["EU_AI_ACT", "IEEE_7000_SERIES"],
    }
    response = client.post("/api/v1/evaluations", json=payload)
    assert response.status_code == 201
    assessment = response.json()
    assert assessment["scenario_id"] == "nlp-clinical-triage-002"
    assert len(assessment["framework_assessments"]) == 2
    assert assessment["overall_risk_tier"] == "HIGH_RISK"
    assert len(assessment["executive_summary"]) > 0


def test_evaluate_scenario_invalid_framework() -> None:
    """EN: Test POST /api/v1/evaluations with unsupported framework returns 400. | ES: Probar que POST /api/v1/evaluations con marco no soportado retorne 400."""
    payload = {
        "scenario_id": "nlp-clinical-triage-002",
        "frameworks": ["INVALID_FRAMEWORK_XYZ"],
    }
    response = client.post("/api/v1/evaluations", json=payload)
    assert response.status_code == 400
