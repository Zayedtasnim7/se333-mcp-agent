# server.py
from __future__ import annotations
import os, re, json, subprocess, sys
from pathlib import Path

# ---- Minimal HTTP MCP server using fastmcp ----
# Tools implemented:
#   - list_java_methods(dir="."): returns found class + method names
#   - generate_basic_junit(class_name, method_name): creates a JUnit 5 skeleton
#   - mvn_test(dir="sample-maven"): runs `mvn -q -e test` and returns summary

try:
    from fastmcp import FastMCP
except ImportError:
    print("fastmcp not installed. Run: python -m pip install fastmcp \"mcp[cli]\" httpx", file=sys.stderr)
    sys.exit(1)

app = FastMCP("se333-mcp-agent")

def _scan_java_methods(root: Path) -> list[dict]:
    results = []
    for p in root.rglob("*.java"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        # naive class + method scan (good enough for demo)
        cls = None
        m = re.search(r"\bclass\s+([A-Za-z_]\w*)", text)
        if m:
            cls = m.group(1)
        for m in re.finditer(r"(public|protected|private|\s) +[A-Za-z_<>\[\]]+\s+([a-zA-Z_]\w*)\s*\(", text):
            method = m.group(2)
            if method not in ("if", "for", "while", "switch", "catch"):
                results.append({"file": str(p), "class": cls, "method": method})
    return results

@app.tool()
def list_java_methods(dir: str = ".") -> list[dict]:
    """
    Recursively list Java methods under `dir`. Returns [{file, class, method}].
    """
    root = Path(dir).resolve()
    if not root.exists():
        return [{"error": f"path not found: {root}"}]
    return _scan_java_methods(root)

@app.tool()
def generate_basic_junit(class_name: str, method_name: str, dir: str = "sample-maven") -> dict:
    """
    Creates a basic JUnit 5 test skeleton for class_name.method_name in sample project.
    """
    proj = Path(dir).resolve()
    test_dir = proj / "src" / "test" / "java" / "org" / "example"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / f"{class_name}Test.java"

    template = f"""\
package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class {class_name}Test {{

    @Test
    void {method_name}_basic() {{
        // TODO: arrange
        {class_name} c = new {class_name}();
        // TODO: act
        // var result = c.{method_name}(/* args */);
        // TODO: assert
        // assertEquals(expected, result);
        assertTrue(true);
    }}
}}
"""
    old = test_file.read_text(encoding="utf-8") if test_file.exists() else ""
    if template.strip() not in old:
        with test_file.open("a", encoding="utf-8") as f:
            if old and not old.endswith("\n"):
                f.write("\n")
            f.write(template)
    return {"created_or_updated": str(test_file)}

@app.tool()
def mvn_test(dir: str = "sample-maven") -> dict:
    """
    Runs `mvn -q -e test` in `dir` and returns a short summary + tail of output.
    """
    proj = Path(dir).resolve()
    if not (proj / "pom.xml").exists():
        return {"error": f"No pom.xml in {proj}"}
    try:
        cp = subprocess.run(
            ["mvn", "-q", "-e", "test"],
            cwd=str(proj),
            capture_output=True,
            text=True
        )
        out = (cp.stdout or "") + "\n" + (cp.stderr or "")
        tail = "\n".join(out.splitlines()[-60:])  # last 60 lines
        return {"returncode": cp.returncode, "tail": tail}
    except FileNotFoundError:
        return {"error": "Maven not found. Install Maven and ensure 'mvn' is on PATH."}
'''''
if __name__ == "__main__":
    # Run as an HTTP server; it prints the URL you need for VS Code.
    # If you need a fixed port, set FASTMCP_PORT env or change default below.
    port = int(os.getenv("FASTMCP_PORT", "0"))  # 0 = auto-pick free port
    url = app.serve_http(host="127.0.0.1", port=port)  # <-- prints usable URL
    print(url, flush=True)
    # Keep process alive
    app.wait_forever()
'''
#-----------------------------------------------


@app.tool()
def mvn_coverage(dir: str = "sample-maven") -> dict:
    """
    Runs `mvn test jacoco:report` and returns coverage report path + summary.
    """
    import subprocess
    from pathlib import Path

    project = Path(dir).resolve()
    if not (project / "pom.xml").exists():
        return {"error": f"No pom.xml found in {project}"}

    cp = subprocess.run(
        ["mvn", "-q", "-e", "test", "jacoco:report"],
        cwd=str(project),
        capture_output=True,
        text=True
    )
    out = (cp.stdout or "") + "\n" + (cp.stderr or "")
    tail = "\n".join(out.splitlines()[-50:])
    report = project / "target" / "site" / "jacoco" / "index.html"
    return {"returncode": cp.returncode, "report": str(report), "log": tail}

#-----------------------------------------------
import subprocess
from pathlib import Path

def _run(cmd, cwd: Path) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    out = (cp.stdout or "") + (cp.stderr or "")
    return cp.returncode, out

@app.tool()
def git_status(dir: str = ".") -> dict:
    """
    Returns clean status and lists staged/unstaged/untracked files.
    """
    repo = Path(dir).resolve()
    code, out = _run(["git", "status", "--porcelain=v1", "--branch"], repo)
    if code != 0:
        return {"error": out.strip()}
    staged, changed, untracked = [], [], []
    for line in out.splitlines():
        if line.startswith("##"):
            continue
        if line.startswith("??"):
            untracked.append(line[3:])
        elif line[:2].strip():  # staged changes have a non-space in first col
            staged.append(line[3:])
        else:
            changed.append(line[3:])
    return {"staged": staged, "changed": changed, "untracked": untracked, "raw": out}

@app.tool()
def git_add_all(dir: str = ".") -> dict:
    """
    Stages all changes (respects .gitignore).
    """
    repo = Path(dir).resolve()
    code, out = _run(["git", "add", "-A"], repo)
    if code != 0:
        return {"error": out.strip()}
    # Show what is staged now
    code2, out2 = _run(["git", "status", "--porcelain=v1"], repo)
    staged = [ln[3:] for ln in out2.splitlines() if ln and ln[0] != "?" and ln[0] != " "]
    return {"staged_count": len(staged), "staged": staged}

@app.tool()
def git_commit(message: str, dir: str = ".") -> dict:
    """
    Commits staged changes with a message. Returns short commit hash.
    """
    repo = Path(dir).resolve()
    # no staged changes?
    code, out = _run(["git", "diff", "--cached", "--name-only"], repo)
    if code != 0:
        return {"error": out.strip()}
    if not out.strip():
        return {"error": "No staged changes to commit."}
    code2, out2 = _run(["git", "commit", "-m", message], repo)
    if code2 != 0:
        return {"error": out2.strip()}
    code3, out3 = _run(["git", "rev-parse", "--short", "HEAD"], repo)
    return {"commit": out3.strip()}

@app.tool()
def git_push(remote: str = "origin", branch: str = "main", dir: str = ".") -> dict:
    """
    Pushes the current branch. Assumes credentials/manager are set up.
    """
    repo = Path(dir).resolve()
    code, out = _run(["git", "push", "-u", remote, branch], repo)
    if code != 0:
        return {"error": out.strip()}
    return {"result": out.strip()}

@app.tool()
def git_pull_request(base: str = "main", title: str = "Auto PR", body: str = "", dir: str = ".") -> dict:
    """
    Creates a PR using GitHub CLI if installed. Returns PR URL, else guidance.
    """
    repo = Path(dir).resolve()
    # detect current branch
    code_b, out_b = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    if code_b != 0:
        return {"error": out_b.strip()}
    head = out_b.strip()
    # check gh
    code_v, _ = _run(["gh", "--version"], repo)
    if code_v != 0:
        return {
            "error": "GitHub CLI (gh) not installed.",
            "how_to_install": "https://cli.github.com/",
            "manual_alternative": "Open a PR on GitHub from branch '{}' into '{}'.".format(head, base),
        }
    code_pr, out_pr = _run(["gh", "pr", "create", "--base", base, "--head", head, "-t", title, "-b", body], repo)
    if code_pr != 0:
        return {"error": out_pr.strip()}
    return {"pr": out_pr.strip()}

#-----------------------------------------------
if __name__ == "__main__":
    # Serve over HTTP so VS Code can connect.
    # URL to paste in VS Code = http://127.0.0.1:6060/mcp
    app.run(transport="http", host="127.0.0.1", port=6061, path="/mcp")

