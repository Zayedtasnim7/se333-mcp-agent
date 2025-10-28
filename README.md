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
- 🔁 **Git Automation Tools** — `git_status`, `git_add_all`, `git_commit(include_coverage)`, `git_push`, `git_pull_request`.
- 🧩 **FastMCP + VS Code Chat** — use the tools from the Chat panel with auto-approve.

### Tech Stack
**Python (FastMCP), Java (Maven/JUnit 5), JaCoCo, GitHub Actions, VS Code**





## Run
.\.venv\Scripts\Activate.ps1
python server.py  # URL: http://127.0.0.1:6060/mcp  (Add via VS Code: MCP: Add Server)
