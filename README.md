# SE333 MCP Testing Agent

[![Maven CI](https://github.com/Zayedtasnim7/se333-mcp-agent/actions/workflows/maven.yml/badge.svg)](https://github.com/Zayedtasnim7/se333-mcp-agent/actions/workflows/maven.yml)

[![Maven CI](https://github.com/Zayedtasnim7/se333-mcp-agent/actions/workflows/maven.yml/badge.svg)](https://github.com/Zayedtasnim7/se333-mcp-agent/actions/workflows/maven.yml)

FastMCP server + tools:
- list_java_methods(dir="sample-maven")
- generate_basic_junit(class_name="Calc", method_name="add")
- mvn_test(dir="sample-maven")

## Highlights
- 🤖 **AI Testing Agent (MCP)** — analyzes Java source, generates JUnit 5 tests, and runs them.
- ✅ **CI/CD with GitHub Actions** — automatic `mvn test` on every push/PR.


- 📈 **JaCoCo Coverage** — reports and HTML site; agent can summarize coverage in chat.


## 2. Coverage Statistics // do i need before and after? 

### Latest Coverage (from sample-maven/target/site/jacoco/jacoco.xml)

- Instruction Coverage: 100% (7/7)
- Line Coverage: 100% (2/2)
- Complexity Coverage: 100% (2/2)
- Method Coverage: 100% (2/2)
- Class Coverage: 100% (1/1)



- 🔁 **Git Automation Tools** — `git_status`, `git_add_all`, `git_commit(include_coverage)`, `git_push`, `git_pull_request`.
- 🧩 **FastMCP + VS Code Chat** — use the tools from the Chat panel with auto-approve.

### Tech Stack
**Python (FastMCP), Java (Maven/JUnit 5), JaCoCo, GitHub Actions, VS Code**


## Quickstart
```bash
# clone
git clone https://github.com/Zayedtasnim7/se333-mcp-agent
cd se333-mcp-agent

# python env (uv or pip)
uv venv && uv pip install fastmcp "mcp[cli]" httpx
# OR: python -m venv .venv && .\.venv\Scripts\activate && pip install fastmcp "mcp[cli]" httpx

# run MCP server (prints URL)
python server.py   # default http://127.0.0.1:6060/mcp

# VS Code → Cmd/Ctrl+Shift+P → "MCP: Add Server" → paste URL
# Ask in Chat: list_java_methods(dir="sample-maven/src/main/java")

## MCP Tool Catalog




| Tool | Purpose | Example |
|---|---|---|
| `list_java_methods(dir)` | scan Java classes/methods | `list_java_methods("sample-maven/src/main/java")` |
| `generate_basic_junit(class_name, method_name, dir)` | create JUnit 5 skeleton | `generate_basic_junit("Calc","add","sample-maven")` |
| `mvn_test(dir)` | run unit tests | `mvn_test("sample-maven")` |
| `mvn_coverage(dir)` | run tests + JaCoCo | `mvn_coverage("sample-maven")` |
| `parse_jacoco(xml_path)` | parse JaCoCo XML | `parse_jacoco("sample-maven/.../jacoco.xml")` |
| `coverage_summary(dir)` | one-shot coverage summary | `coverage_summary("sample-maven")` |
| `git_status(dir)` | git status summary | `git_status()` |
| `git_add_all(dir)` | stage changes | `git_add_all()` |
| `git_commit(message, include_coverage, coverage_dir)` | commit with optional coverage stats | `git_commit("feat: add tests", True, "sample-maven")` |
| `git_push(remote, branch, dir)` | push current branch | `git_push()` |
| `git_pull_request(base, title, body, dir)` | open PR via `gh` | `git_pull_request("main","Phase 2: coverage","Adds JaCoCo + parser")` |


## Run
.\.venv\Scripts\Activate.ps1
python server.py  # URL: http://127.0.0.1:6060/mcp  (Add via VS Code: MCP: Add Server)

## Submission artifacts & next steps
The repository now includes the MCP prompt and data needed to build your reflection report.  I've added a small helper to generate the LaTeX reflection file from the metrics we already collected.

- `.github/prompts/tester.prompt.md` — MCP agent prompt used by the VS Code Chat/Auto-Approve setup.
- `docs/reflection-data.md` — cleaned project metrics and data used to populate the reflection.
- `docs/my_project_metrics.txt` — generated metrics (coverage, tests, git snapshot).
- `build_reflection_tex.py` — script to generate the LaTeX reflection from the files above.
- `report/reflection.tex` — generated LaTeX (IEEEtran) for the 2-page reflection report.

How to generate the LaTeX reflection:

```powershell
# from project root
python build_reflection_tex.py --data docs/reflection-data.md --metrics docs/my_project_metrics.txt --out report/reflection.tex
```

To compile to PDF (if you have LaTeX installed):

```powershell
# compile into report/reflection.pdf
pdflatex -output-directory report report/reflection.tex
```

Recommended submission structure (final_project_se333_{name}/):

```
final_project_se333_{name}/
├── codebase/ # Project that you analyzed (this repo)
├── .github/prompts
├── README.md
├── report/
│   └── reflection.pdf   # generated from report/reflection.tex
├── demo/                # final_presentation.mp4 (if recorded)
└── docs/
	└── reflection-data.md
```

Checklist before submitting:

1. Feature implemented and committed (use a clear git message, e.g. `feat: add reflection generator`).
2. `README.md` includes setup & MCP tool docs.
3. `report/reflection.pdf` uploaded to `/report/` (or compile locally and add it before pushing).
4. `demo/final_presentation.mp4` uploaded (if applicable).
5. Coverage results (JaCoCo) included or demonstrated in your video.

If you'd like, I can also:
- Compile `report/reflection.tex` to PDF here if a TeX tool is available in the environment.
- Create a short demo script or record a step-by-step run for you to use in the final video.

Demo runner

A small demo runner script exists in `scripts/demo_runner.py` (use same venv as server). It performs these steps programmatically and helps you record the flow:

1. `coverage_summary("sample-maven")`
2. `find_uncovered_methods("sample-maven")`
3. `generate_basic_junit(...)` for the first uncovered method (if any)
4. `mvn_test("sample-maven")`
5. `coverage_summary("sample-maven")`

Run it with your virtualenv activated:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/demo_runner.py
```

Enforcement workflow

There is an optional GitHub Action that can check for required submission artifacts. If you prefer a non-blocking reviewer comment instead of failing the PR, I can adjust that workflow.
