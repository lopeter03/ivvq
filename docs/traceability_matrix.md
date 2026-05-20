# Traceability Matrix

| **BR ID** | **Business Requirement** | **FS ID** | **Functional Specification** | **TC ID** | **Test Case** |
| --- | --- | --- | --- | --- | --- |
| BR1 | API must respond with correct status code | FS1 | REST API returns HTTP 200 at ``/api/hello`` | TC1 | Verify API response code = 200 |
| BR2 | API must return mandatory payload fields | FS2 | JSON contains ``"message":"Hello ``World"`` | TC2 | Verify API response body matches expected |
| BR3 | Deployment must be automated | FS3 | Ansible playbook installs Flask & runs API | TC3 | Run playbook, confirm API starts successfully |
| BR4 | Test results must be documented | FS4 | Pytest generates JUnit XML report in ``/reports/results.xml`` | TC4 | Verify report file exists with PASS results |
| BR5 | Requirements must be traceable | FS5 | Matrix links BR → FS → TC in ``requirements/traceability_matrix.md`` | TC5 | Manual check of matrix completeness |