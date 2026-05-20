import subprocess
import datetime
import os
import shutil

# Anchor paths to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # D:\project\ivvq\tests
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)                # D:\project\ivvq
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
REPORTS_DIR = os.path.join(TESTS_DIR, "reports")           # ✅ Only under tests/reports

# Pre-define results.xml path to avoid root-level reports
RESULTS_XML = os.path.join(REPORTS_DIR, "results.xml")

def run_command(cmd, use_wsl=False):
    if use_wsl:
        cmd = f"wsl {cmd}"
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",      # force UTF-8 decoding
        errors="replace"       # replace bad bytes instead of crashing
    )

TEST_CASES = [
    {
        "id": "TC1",
        "description": "Verify API responds with Hello World (FS1)",
        "expected": "HTTP 200 and message body {\"message\":\"Hello World\"}",
        "command": "curl -s -w '\\nHTTP_CODE:%{http_code}' http://127.0.0.1:5000/api/hello",
        "use_wsl": True,
        "validator": lambda out: "Hello World" in out and "HTTP_CODE:200" in out
    },
    {
        "id": "TC2",
        "description": "Verify API handles invalid route (FS2)",
        "expected": "HTTP 404 for invalid endpoint",
        "command": "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/api/invalid",
        "use_wsl": True,
        "validator": lambda out: "404" in out
    },
    {
        "id": "TC3",
        "description": "Verify Ansible playbook deploys API (FS3)",
        "expected": "Play recap shows ok with no failures",
        "command": f"ansible-playbook /mnt/d/project/ivvq/ansible/playbook.yml",
        "use_wsl": True,
        "validator": lambda out: "PLAY RECAP" in out and "failed=0" in out
    },
    {
        "id": "TC4",
        "description": "Verify pytest generates XML report (FS4)",
        "expected": "tests/reports/results.xml created and tests pass",
        "command": f"pytest {os.path.join(TESTS_DIR, 'test_api.py')} --junitxml={RESULTS_XML} -s",
        "use_wsl": False,
        "validator": lambda out: os.path.exists(RESULTS_XML)
    },
    {
        "id": "TC5",
        "description": "Verify traceability matrix exists (FS5)",
        "expected": "File docs/traceability_matrix.md exists",
        "command": f"test -f /mnt/d/project/ivvq/docs/traceability_matrix.md && echo Found || echo Missing",
        "use_wsl": True,
        "validator": lambda out: "Found" in out
    }
]

# ✅ Report now goes under tests/reports
REPORT_FILE = os.path.join(REPORTS_DIR, "test_execution_detailed.md")

def run_test(tc):
    print(f"Running {tc['id']} - {tc['description']}")
    result = run_command(tc["command"], use_wsl=tc["use_wsl"])
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    status = "PASS" if tc["validator"](stdout) else "FAIL"
    return {
        "id": tc["id"],
        "description": tc["description"],
        "expected": tc["expected"],
        "command": tc["command"],
        "stdout": stdout or "None",
        "stderr": stderr or "None",
        "status": status,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)  # ensure tests/reports exists
    results = [run_test(tc) for tc in TEST_CASES]

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("📑 Detailed Test Execution Report (TC1–TC5)\n")
        f.write("="*80 + "\n\n")
        for r in results:
            f.write(f"Test ID: {r['id']}\n")
            f.write(f"Description: {r['description']}\n")
            f.write(f"Expected Result: {r['expected']}\n")
            f.write(f"Command Executed: {r['command']}\n")
            f.write(f"Timestamp: {r['timestamp']}\n")
            f.write(f"Status: {r['status']}\n")
            f.write("---- Stdout ----\n")
            f.write(r['stdout'] + "\n")
            f.write("---- Stderr ----\n")
            f.write(r['stderr'] + "\n")
            f.write("-"*80 + "\n\n")

        # 📊 Append summary at the end
        total_tests = len(results)
        pass_count = sum(1 for r in results if r["status"] == "PASS")
        fail_count = sum(1 for r in results if r["status"] == "FAIL")
        success_rate = (pass_count / total_tests) * 100 if total_tests > 0 else 0

        f.write("="*80 + "\n")
        f.write("📊 Execution Summary\n")
        f.write(f"- Total Tests: {total_tests}\n")
        f.write(f"- PASS: {pass_count}\n")
        f.write(f"- FAIL: {fail_count}\n")
        f.write(f"- Success Rate: {success_rate:.1f}%\n")
        if fail_count == 0:
            f.write("✅ All tests passed\n")
        else:
            f.write("❌ Some tests failed\n")

    print(f"✅ Report generated: {REPORT_FILE}")

    # 🔓 Auto-open the report in Notepad
    try:
        subprocess.Popen(["notepad.exe", REPORT_FILE])
    except Exception as e:
        print(f"⚠️ Could not auto-open report in Notepad: {e}")

    # 🧹 Cleanup: remove unwanted root-level reports directory if it exists
    unwanted_dir = os.path.join(PROJECT_ROOT, "reports")
    if os.path.exists(unwanted_dir):
        try:
            shutil.rmtree(unwanted_dir)
            print(f"🗑️ Removed unwanted directory: {unwanted_dir}")
        except Exception as e:
            print(f"⚠️ Could not remove {unwanted_dir}: {e}")

if __name__ == "__main__":
    main()
