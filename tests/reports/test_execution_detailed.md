📑 Detailed Test Execution Report (TC1–TC5)
================================================================================

Test ID: TC1
Description: Verify API responds with Hello World (FS1)
Expected Result: HTTP 200 and message body {"message":"Hello World"}
Command Executed: curl -s -w '\nHTTP_CODE:%{http_code}' http://127.0.0.1:5000/api/hello
Timestamp: 2026-05-20 14:22:08
Status: PASS
---- Stdout ----
{"message":"Hello World"}

HTTP_CODE:200
---- Stderr ----
None
--------------------------------------------------------------------------------

Test ID: TC2
Description: Verify API handles invalid route (FS2)
Expected Result: HTTP 404 for invalid endpoint
Command Executed: curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/api/invalid
Timestamp: 2026-05-20 14:22:08
Status: PASS
---- Stdout ----
404
---- Stderr ----
None
--------------------------------------------------------------------------------

Test ID: TC3
Description: Verify Ansible playbook deploys API (FS3)
Expected Result: Play recap shows ok with no failures
Command Executed: ansible-playbook /mnt/d/project/ivvq/ansible/playbook.yml
Timestamp: 2026-05-20 14:22:13
Status: PASS
---- Stdout ----
PLAY [Deploy API and run tests] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Start API] ***************************************************************
changed: [localhost]

TASK [Run tests] ***************************************************************
changed: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
---- Stderr ----
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
--------------------------------------------------------------------------------

Test ID: TC4
Description: Verify pytest generates XML report (FS4)
Expected Result: tests/reports/results.xml created and tests pass
Command Executed: pytest D:\project\ivvq\tests\test_api.py --junitxml=D:\project\ivvq\tests\reports\results.xml -s
Timestamp: 2026-05-20 14:22:14
Status: PASS
---- Stdout ----
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
rootdir: D:\project\ivvq\tests
plugins: anyio-4.13.0, base-url-2.1.0, html-4.1.1, json-report-1.5.0, metadata-3.1.1, playwright-0.8.0
collected 4 items

test_api.py FS1 Outcome: HTTP Status Code = 200
.FS2 Outcome: Response Body = {'message': 'Hello World'}
.FS3 Outcome: API accessible, deployment validated
.FS5 Outcome: traceability_matrix.md exists = True (D:\project\ivvq\docs\traceability_matrix.md)
.

-------- generated xml file: D:\project\ivvq\tests\reports\results.xml --------
============================== 4 passed in 0.20s ==============================
---- Stderr ----
None
--------------------------------------------------------------------------------

Test ID: TC5
Description: Verify traceability matrix exists (FS5)
Expected Result: File docs/traceability_matrix.md exists
Command Executed: test -f /mnt/d/project/ivvq/docs/traceability_matrix.md && echo Found || echo Missing
Timestamp: 2026-05-20 14:22:15
Status: PASS
---- Stdout ----
Found
---- Stderr ----
None
--------------------------------------------------------------------------------

================================================================================
📊 Execution Summary
- Total Tests: 5
- PASS: 5
- FAIL: 0
- Success Rate: 100.0%
✅ All tests passed
