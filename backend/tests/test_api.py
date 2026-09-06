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


# EN: Case Studies Endpoint Tests | ES: Pruebas de Puntos Finales de Casos de Estudio


def test_get_cases_endpoint() -> None:
    """EN: Test GET /api/v1/cases returns the three complex NLP case studies. | ES: Probar que GET /api/v1/cases retorne los tres casos de estudio complejos de NLP."""
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) == 3
    case_ids = [c["id"] for c in cases]
    assert "cs-recruitment-llm-001" in case_ids
    assert "cs-forensic-stylometry-002" in case_ids
    assert "cs-dataset-provenance-003" in case_ids


def test_get_case_detail_success() -> None:
    """EN: Test GET /api/v1/cases/{id} returns complete case study specification. | ES: Probar que GET /api/v1/cases/{id} retorne la especificacion completa del caso de estudio."""
    response = client.get("/api/v1/cases/cs-recruitment-llm-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "cs-recruitment-llm-001"
    assert len(data["decision_options"]) == 3
    assert "FAIRNESS" in data["baseline_matrix"]
    assert len(data["linguistic_artifacts"]) == 4


def test_get_case_detail_not_found() -> None:
    """EN: Test GET /api/v1/cases/{id} returns 404 for missing case study. | ES: Probar que GET /api/v1/cases/{id} retorne 404 para caso de estudio faltante."""
    response = client.get("/api/v1/cases/unknown-case-id")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "CASE_STUDY_NOT_FOUND"


# EN: Decision Submission Endpoint Tests | ES: Pruebas de Punto Final de Envio de Decisiones


def test_submit_decision_endpoint_success() -> None:
    """EN: Test POST /api/v1/decisions successfully evaluates decision impact. | ES: Probar que POST /api/v1/decisions evalue exitosamente el impacto de la decision."""
    payload = {
        "case_id": "cs-recruitment-llm-001",
        "selected_option_id": "opt-recruit-fairness-oversight",
        "user_rationale": "Mandatory human recruiter oversight with counterfactual fairness audit.",
        "frameworks": ["EU_AI_ACT", "IEEE_7000_SERIES"],
    }
    response = client.post("/api/v1/decisions", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["case_id"] == "cs-recruitment-llm-001"
    assert data["selected_option"]["id"] == "opt-recruit-fairness-oversight"
    assert "matrix" in data
    assert data["matrix"]["fairness"]["delta"] > 0
    assert len(data["framework_assessments"]) == 2
    assert len(data["trade_off_analysis"]) > 20
    assert len(data["recommendations"]) > 0

    # EN: Test GET /api/v1/evaluations/{id} retrieves saved result | ES: Probar que GET /api/v1/evaluations/{id} recupere el resultado guardado
    decision_id = data["decision_id"]
    eval_response = client.get(f"/api/v1/evaluations/{decision_id}")
    assert eval_response.status_code == 200
    eval_data = eval_response.json()
    assert eval_data["decision_id"] == decision_id


def test_get_evaluation_not_found() -> None:
    """EN: Test GET /api/v1/evaluations/{id} returns 404 for unknown evaluation. | ES: Probar que GET /api/v1/evaluations/{id} retorne 404 para evaluacion desconocida."""
    response = client.get("/api/v1/evaluations/unknown-eval-12345")
    assert response.status_code == 404


# EN: Scenarios Compatibility Tests | ES: Pruebas de Compatibilidad de Escenarios


def test_list_scenarios_endpoint() -> None:
    """EN: Test GET /api/v1/scenarios retrieves scenarios. | ES: Probar que GET /api/v1/scenarios recupere los escenarios."""
    response = client.get("/api/v1/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) >= 3


def test_get_single_scenario_success() -> None:
    """EN: Test GET /api/v1/scenarios/{id} returns scenario detail. | ES: Probar que GET /api/v1/scenarios/{id} retorne el detalle del escenario."""
    response = client.get("/api/v1/scenarios/cs-recruitment-llm-001")
    assert response.status_code == 200
    scenario = response.json()
    assert scenario["id"] == "cs-recruitment-llm-001"
    assert len(scenario["artifacts"]) > 0


def test_evaluate_scenario_success() -> None:
    """EN: Test POST /api/v1/evaluations executes assessment and returns 201. | ES: Probar que POST /api/v1/evaluations ejecute la evaluacion y retorne 201."""
    payload = {
        "scenario_id": "cs-recruitment-llm-001",
        "frameworks": ["EU_AI_ACT", "IEEE_7000_SERIES"],
    }
    response = client.post("/api/v1/evaluations", json=payload)
    assert response.status_code == 201
    assessment = response.json()
    assert assessment["scenario_id"] == "cs-recruitment-llm-001"
    assert len(assessment["framework_assessments"]) == 2
