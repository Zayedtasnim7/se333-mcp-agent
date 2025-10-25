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

if __name__ == "__main__":
    # Serve over HTTP so VS Code can connect.
    # URL to paste in VS Code = http://127.0.0.1:6060/mcp
    app.run(transport="http", host="127.0.0.1", port=6060, path="/mcp")
