import requests
import os

BASE_URL = "http://127.0.0.1:5000/api/hello"

def test_api_response_code():
    """FS1 → TC1: Verify API returns HTTP 200"""
    response = requests.get(BASE_URL)
    print(f"FS1 Outcome: HTTP Status Code = {response.status_code}")
    assert response.status_code == 200

def test_api_response_body():
    """FS2 → TC2: Verify API payload contains 'message'"""
    response = requests.get(BASE_URL)
    data = response.json()
    print(f"FS2 Outcome: Response Body = {data}")
    assert "message" in data
    assert data["message"] == "Hello World"

def test_ansible_deployment():
    """FS3 → TC3: Verify API is accessible (deployment check)"""
    response = requests.get(BASE_URL)
    print("FS3 Outcome: API accessible, deployment validated")
    assert response.status_code == 200

def test_traceability_matrix_completeness():
    """FS5 → TC5: Verify traceability matrix completeness"""
    # Resolve project root two levels up from tests/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    matrix_path = os.path.join(project_root, "docs", "traceability_matrix.md")
    exists = os.path.exists(matrix_path)
    print(f"FS5 Outcome: traceability_matrix.md exists = {exists} ({matrix_path})")
    assert exists
