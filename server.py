# server.py
from __future__ import annotations
import os, re, json, subprocess, sys, shlex
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# ============== MCP bootstrap ==============
try:
    from fastmcp import FastMCP
except ImportError:
    print(
        "fastmcp not installed. Run:\n  uv add mcp[cli] httpx fastmcp\n  # or: python -m pip install 'fastmcp' 'mcp[cli]' httpx",
        file=sys.stderr,
    )
    sys.exit(1)

app = FastMCP("se333-mcp-agent")


# ============== small helpers ==============
def _run(cmd: List[str], cwd: Path) -> Tuple[int, str]:
    """Run a command and return (returncode, stdout+stderr)."""
    cp = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    out = (cp.stdout or "") + (cp.stderr or "")
    return cp.returncode, out


def _exists(cmd: str) -> bool:
    """Rough check that a command is available on PATH."""
    which = "where" if os.name == "nt" else "which"
    try:
        return subprocess.run([which, cmd], capture_output=True).returncode == 0
    except Exception:
        return False


# ============== Java scanning & test gen ==============
def _scan_java_methods(root: Path) -> List[Dict]:
    results: List[Dict] = []
    for p in root.rglob("*.java"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # naive class + method scan (demo-OK)
        cls = None
        m = re.search(r"\bclass\s+([A-Za-z_]\w*)", text)
        if m:
            cls = m.group(1)
        for m in re.finditer(r"(public|protected|private|\s)+[A-Za-z_<>\[\]]+\s+([a-zA-Z_]\w*)\s*\(", text):
            method = m.group(2)
            if method not in ("if", "for", "while", "switch", "catch"):
                results.append({"file": str(p), "class": cls, "method": method})
    return results


@app.tool()
def list_java_methods(dir: str = ".") -> List[Dict]:
    """
    Recursively list Java methods under `dir`. Returns [{file, class, method}].
    """
    root = Path(dir).resolve()
    if not root.exists():
        return [{"error": f"path not found: {root}"}]
    return _scan_java_methods(root)


@app.tool()
def generate_basic_junit(class_name: str, method_name: str, dir: str = "sample-maven") -> Dict:
    """
    Creates/updates a basic JUnit 5 test skeleton for class_name.method_name in sample project.
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
        // arrange
        {class_name} c = new {class_name}();
        // act
        // var result = c.{method_name}(/* args */);
        // assert
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


# ============== Maven test & coverage ==============
@app.tool()
def mvn_test(dir: str = "sample-maven") -> Dict:
    """
    Runs `mvn -q -e test` in `dir` and returns {returncode, tail}.
    """
    proj = Path(dir).resolve()
    if not (proj / "pom.xml").exists():
        return {"error": f"No pom.xml in {proj}"}
    if not _exists("mvn"):
        return {"error": "Maven not found. Install Maven and ensure 'mvn' is on PATH."}

    code, out = _run(["mvn", "-q", "-e", "test"], proj)
    tail = "\n".join(out.splitlines()[-60:])
    return {"returncode": code, "tail": tail}


@app.tool()
def mvn_coverage(dir: str = "sample-maven") -> Dict:
    """
    Runs `mvn test jacoco:report` and returns report path + log tail.
    """
    project = Path(dir).resolve()
    if not (project / "pom.xml").exists():
        return {"error": f"No pom.xml in {project}"}
    if not _exists("mvn"):
        return {"error": "Maven not found. Install Maven and ensure 'mvn' is on PATH."}

    code, out = _run(["mvn", "-q", "-e", "test", "jacoco:report"], project)
    tail = "\n".join(out.splitlines()[-60:])
    report_html = project / "target" / "site" / "jacoco" / "index.html"
    report_xml = project / "target" / "site" / "jacoco" / "jacoco.xml"
    return {
        "returncode": code,
        "report_html": str(report_html),
        "report_xml": str(report_xml),
        "log_tail": tail,
    }


@app.tool()
def parse_jacoco(xml_path: str = "sample-maven/target/site/jacoco/jacoco.xml") -> Dict:
    """
    Parses a JaCoCo XML and returns coverage percentages by counter type.
    """
    from xml.etree import ElementTree as ET

    xml = Path(xml_path).resolve()
    if not xml.exists():
        return {"error": f"Coverage XML not found: {xml}"}

    tree = ET.parse(xml)
    counters = tree.findall(".//counter")
    data: Dict[str, Dict[str, int]] = {}
    for c in counters:
        t = c.get("type", "UNKNOWN")
        covered = int(c.get("covered", "0"))
        missed = int(c.get("missed", "0"))
        data[t] = {"covered": covered, "missed": missed}

    summary = {}
    for t, cm in data.items():
        tot = cm["covered"] + cm["missed"]
        pct = (cm["covered"] / tot * 100.0) if tot else 0.0
        summary[t] = round(pct, 2)

    # Friendly short fields
    line = summary.get("LINE")
    branch = summary.get("BRANCH")
    return {"summary": summary, "line": line, "branch": branch, "xml": str(xml)}


@app.tool()
def coverage_summary(dir: str = "sample-maven") -> Dict:
    """
    Runs coverage then parses the XML and returns {line, branch, summary, report_html}.
    """
    run = mvn_coverage(dir)  # type: ignore
    if "error" in run:
        return run
    parsed = parse_jacoco(str(Path(run["report_xml"]))).copy()  # type: ignore
    parsed["report_html"] = run["report_html"]                  # type: ignore
    return parsed


# ============== Git automation tools ==============
@app.tool()
def git_status(dir: str = ".") -> Dict:
    """
    Returns staged/changed/untracked and raw status.
    """
    repo = Path(dir).resolve()
    if not _exists("git"):
        return {"error": "git not found on PATH."}
    code, out = _run(["git", "status", "--porcelain=v1", "--branch"], repo)
    if code != 0:
        return {"error": out.strip()}

    staged, changed, untracked = [], [], []
    for line in out.splitlines():
        if line.startswith("##"):  # branch line
            continue
        if line.startswith("??"):
            untracked.append(line[3:])
        elif line[:1] != " " and line[:1] != "?":  # first col non-space => staged
            staged.append(line[3:])
        else:
            # includes modified but unstaged, deleted, etc.
            changed.append(line[3:])

    return {"staged": staged, "changed": changed, "untracked": untracked, "raw": out}


@app.tool()
def git_add_all(dir: str = ".") -> Dict:
    """
    Stages all changes (respects .gitignore). Returns staged list.
    """
    repo = Path(dir).resolve()
    if not _exists("git"):
        return {"error": "git not found on PATH."}
    code, out = _run(["git", "add", "-A"], repo)
    if code != 0:
        return {"error": out.strip()}
    code2, out2 = _run(["git", "status", "--porcelain=v1"], repo)
    if code2 != 0:
        return {"error": out2.strip()}
    staged = [ln[3:] for ln in out2.splitlines() if ln and ln[0] not in ("?", " ")]
    return {"staged_count": len(staged), "staged": staged}


@app.tool()
def git_commit(message: str, dir: str = ".", include_coverage: bool = False, coverage_dir: str = "sample-maven") -> Dict:
    """
    Commits staged changes. Optionally appends coverage to the message.
    Returns short commit hash.
    """
    repo = Path(dir).resolve()
    if not _exists("git"):
        return {"error": "git not found on PATH."}

    # ensure something is staged
    code, out = _run(["git", "diff", "--cached", "--name-only"], repo)
    if code != 0:
        return {"error": out.strip()}
    if not out.strip():
        return {"error": "No staged changes to commit."}

    msg = message
    if include_coverage:
        cov = coverage_summary(coverage_dir)
        if "line" in cov and cov.get("line") is not None:
            msg = f"{message} — line: {cov['line']}%, branch: {cov.get('branch') or 'N/A'}%"

    code2, out2 = _run(["git", "commit", "-m", msg], repo)
    if code2 != 0:
        return {"error": out2.strip()}

    code3, out3 = _run(["git", "rev-parse", "--short", "HEAD"], repo)
    return {"commit": out3.strip(), "message": msg}


@app.tool()
def git_push(remote: str = "origin", branch: Optional[str] = None, dir: str = ".") -> Dict:
    """
    Pushes the current branch (or a specified one). Returns push output.
    """
    repo = Path(dir).resolve()
    if not _exists("git"):
        return {"error": "git not found on PATH."}

    if branch is None:
        code_b, out_b = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
        if code_b != 0:
            return {"error": out_b.strip()}
        branch = out_b.strip()

    code, out = _run(["git", "push", "-u", remote, branch], repo)
    if code != 0:
        return {"error": out.strip()}
    return {"result": out.strip(), "branch": branch, "remote": remote}


@app.tool()
def git_pull_request(
    base: str = "main",
    title: str = "Auto PR",
    body: str = "",
    dir: str = ".",
) -> Dict:
    """
    Creates a PR using GitHub CLI (gh) if installed. Returns PR URL or guidance.
    """
    repo = Path(dir).resolve()
    if not _exists("git"):
        return {"error": "git not found on PATH."}

    # current branch
    code_b, out_b = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    if code_b != 0:
        return {"error": out_b.strip()}
    head = out_b.strip()

    # require gh
    if not _exists("gh"):
        return {
            "error": "GitHub CLI (gh) not installed.",
            "how_to_install": "https://cli.github.com/",
            "manual_alternative": f"Open a PR on GitHub: base '{base}' ← compare '{head}'.",
        }

    code_pr, out_pr = _run(
        ["gh", "pr", "create", "--base", base, "--head", head, "-t", title, "-b", body],
        repo,
    )
    if code_pr != 0:
        return {"error": out_pr.strip()}
    return {"pr": out_pr.strip()}

#=================================================

# ============== Phase 4: Intelligent Test Iteration ==============

from xml.etree import ElementTree as ET

def _uncovered_methods_from_jacoco(xml_path: Path) -> list[dict]:
    """
    Parse JaCoCo XML and return a list of methods that still have missed instructions/lines.
    Each item: {package, class, method, desc, missed_instr, missed_lines}
    """
    out: list[dict] = []
    if not xml_path.exists():
        return out
    root = ET.parse(str(xml_path)).getroot()
    # Structure: report/package/class/method/counter
    for pkg in root.findall(".//package"):
        pkg_name = pkg.get("name","")
        for cls in pkg.findall("./class"):
            cls_name = cls.get("name","")
            for m in cls.findall("./method"):
                name = m.get("name","")
                desc = m.get("desc","")
                missed_instr = missed_lines = 0
                for c in m.findall("./counter"):
                    ctype = c.get("type","")
                    missed = int(c.get("missed","0"))
                    if ctype == "INSTRUCTION":
                        missed_instr = missed
                    elif ctype == "LINE":
                        missed_lines = missed
                if (missed_instr > 0) or (missed_lines > 0):
                    out.append({
                        "package": pkg_name,
                        "class": cls_name,
                        "method": name,
                        "desc": desc,
                        "missed_instr": missed_instr,
                        "missed_lines": missed_lines
                    })
    return out


@app.tool()
def find_uncovered_methods(dir: str = "sample-maven") -> dict:
    """
    Runs coverage and lists uncovered methods from JaCoCo.
    Returns {count, items:[{package,class,method,missed_instr,missed_lines}], line, branch}.
    """
    cov = mvn_coverage(dir)  # run tests + report
    if "error" in cov:
        return cov
    xml = Path(cov["report_xml"])
    items = _uncovered_methods_from_jacoco(xml)
    summary = parse_jacoco(str(xml))
    return {"count": len(items), "items": items, "line": summary.get("line"), "branch": summary.get("branch")}


def _ensure_test_exists_for(class_name: str, method_name: str, proj_dir: Path) -> dict:
    """
    Calls generate_basic_junit if a basic test for class/method isn't present yet.
    """
    test_dir = proj_dir / "src" / "test" / "java" / "org" / "example"
    test_file = test_dir / f"{class_name.split('/')[-1]}Test.java"
    if test_file.exists():
        txt = test_file.read_text(encoding="utf-8", errors="ignore")
        sig = f"void {method_name}_basic()"
        if sig in txt:
            return {"created": False, "file": str(test_file)}
    # create or append
    return generate_basic_junit(class_name=class_name.split('/')[-1], method_name=method_name, dir=str(proj_dir))


@app.tool()
def try_fix_known_bugs(dir: str = "sample-maven") -> dict:
    """
    Extremely small demo 'auto-fix':
    - If Calc.add returns a-b, replace with a+b.
    Extend this function with more patterns as needed.
    """
    proj = Path(dir).resolve()
    calc = proj / "src" / "main" / "java" / "org" / "example" / "Calc.java"
    if not calc.exists():
        return {"changed": False, "reason": "Calc.java not found (demo fix pattern)."}
    txt = calc.read_text(encoding="utf-8", errors="ignore")
    new = txt
    # naive pattern: return a - b;  -> return a + b;
    new = re.sub(r"return\s+([a-zA-Z_]\w*)\s*-\s*([a-zA-Z_]\w*)\s*;", r"return \1 + \2;", new)
    if new != txt:
        calc.write_text(new, encoding="utf-8")
        return {"changed": True, "file": str(calc), "fix": "add(): '-' -> '+'"}
    return {"changed": False, "reason": "No known bug pattern found."}


@app.tool()
def iterate_coverage(dir: str = "sample-maven", max_rounds: int = 3) -> dict:
    """
    Iteratively:
      1) run coverage,
      2) pick an uncovered method,
      3) create a basic test (if missing),
      4) run tests; if they fail, try a simple auto-fix and re-run,
      5) repeat up to max_rounds or until fully covered.

    Returns a run log and the final coverage summary.
    """
    proj = Path(dir).resolve()
    history: list[dict] = []

    for round_i in range(1, max_rounds + 1):
        # 1) coverage
        cov = mvn_coverage(dir)
        if "error" in cov:
            history.append({"round": round_i, "action": "coverage_error", "details": cov})
            break

        xml = Path(cov["report_xml"])
        uncovered = _uncovered_methods_from_jacoco(xml)
        parsed = parse_jacoco(str(xml))
        line_pct, br_pct = parsed.get("line"), parsed.get("branch")

        # If nothing left uncovered, we're done.
        if not uncovered:
            history.append({"round": round_i, "action": "done", "coverage": {"line": line_pct, "branch": br_pct}})
            return {"history": history, "final_coverage": {"line": line_pct, "branch": br_pct}}

        # 2) Choose the first uncovered method (simple heuristic)
        target = uncovered[0]
        cls_internal = target["class"]           # e.g., org/example/Calc
        cls_simple = cls_internal.split("/")[-1] # Calc
        method = target["method"]

        # 3) Ensure a basic test exists
        created = _ensure_test_exists_for(cls_internal, method, proj)
        history.append({"round": round_i, "action": "ensure_test", "target": f"{cls_simple}.{method}", "result": created})

        # 4) Run tests
        test_res = mvn_test(dir)
        # capture a short tail
        tail = (test_res.get("tail") or "").splitlines()[-15:]
        history.append({"round": round_i, "action": "mvn_test", "returncode": test_res.get("returncode"), "tail": tail})

        # If tests failed, attempt auto-fix and re-run once
        if test_res.get("returncode", 1) != 0:
            fix = try_fix_known_bugs(dir)
            history.append({"round": round_i, "action": "try_fix_known_bugs", "result": fix})
            if fix.get("changed"):
                test_res2 = mvn_test(dir)
                tail2 = (test_res2.get("tail") or "").splitlines()[-15:]
                history.append({"round": round_i, "action": "mvn_test_after_fix", "returncode": test_res2.get("returncode"), "tail": tail2})

        # 5) continue loop; will re-check coverage next round

    # After max rounds, report current coverage
    final_cov = coverage_summary(dir)
    history.append({"round": "final", "action": "stop", "coverage": {"line": final_cov.get("line"), "branch": final_cov.get("branch")}})
    return {"history": history, "final_coverage": {"line": final_cov.get("line"), "branch": final_cov.get("branch")}}
#=================================================

# ============== server runner ==============
if __name__ == "__main__":
    # HTTP transport for VS Code MCP (stable on Windows).
    # Paste this URL into VS Code: MCP: Add Server
    host = "127.0.0.1"
    port = int(os.getenv("FASTMCP_PORT", "6060"))
    path = "/mcp"
    print(f"Starting MCP server at http://{host}:{port}{path}", flush=True)
    app.run(transport="http", host=host, port=port, path=path)

#==============================================


