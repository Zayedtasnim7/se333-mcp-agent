# SE333 MCP Testing Agent

FastMCP server + tools:
- list_java_methods(dir="sample-maven")
- generate_basic_junit(class_name="Calc", method_name="add")
- mvn_test(dir="sample-maven")

## Run
.\.venv\Scripts\Activate.ps1
python server.py  # URL: http://127.0.0.1:6060/mcp  (Add via VS Code: MCP: Add Server)
