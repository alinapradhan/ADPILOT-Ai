from fastapi.testclient import TestClient

from app.main import app
from tests.fixtures.sample_payloads import INVESTIGATION_REQUEST, PREVIEW_REQUEST


client = TestClient(app)



def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"



def test_preview_and_investigation_workflow() -> None:
    preview = client.post("/analysis/preview", json=PREVIEW_REQUEST, headers={"X-User-Id": "user-1"})
    assert preview.status_code == 200
    preview_data = preview.json()
    assert any(metric["metric"] == "cpa" for metric in preview_data["metrics"])

    investigate = client.post(
        "/analysis/investigate",
        json=INVESTIGATION_REQUEST,
        headers={"X-User-Id": "user-1"},
    )
    assert investigate.status_code == 200
    body = investigate.json()
    assert body["findings"]
    cpa_findings = [item for item in body["findings"] if item["metric"] == "cpa"]
    assert cpa_findings
    assert cpa_findings[0]["current_value"] > cpa_findings[0]["comparison_value"]



def test_authorization_enforced() -> None:
    response = client.post("/analysis/preview", json=PREVIEW_REQUEST, headers={"X-User-Id": "user-2"})
    assert response.status_code == 403
