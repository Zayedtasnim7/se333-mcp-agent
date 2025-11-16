SE333 Final Project — Demo Script & Recording Checklist

Goal: Record a 4–6 minute demo that shows the MCP testing agent in action and the coverage improvements.

Suggested clips (ordered):

1. Introduction (15–30s)
   - Title slide or quick voice intro: "SE333 final project — MCP testing agent" and your name.
   - Briefly state what you will show: starting the MCP server, generating a test, running tests, and coverage report.

2. Start MCP server (20–40s)
   - Show terminal where you activate the Python venv and run `python server.py`.
   - Show the printed MCP URL (http://127.0.0.1:6060/mcp).
   - In VS Code, open Chat → MCP: Add Server and paste the URL (optional: show tools list).

3. Find uncovered methods (30–45s)
   - In the VS Code Chat for the MCP server, run: `find_uncovered_methods(dir="sample-maven")`.
   - Show the returned uncovered methods and coverage summary (line/branch %).

4. Generate a basic test (30–45s)
   - Use the tool: `generate_basic_junit(class_name="Calc", method_name="add", dir="sample-maven")` (or generate for an uncovered method listed earlier).
   - Show the created test file in the editor (open `sample-maven/src/test/java/...`).

5. Run tests and coverage (30–45s)
   - Run `mvn_test(dir="sample-maven")` from the MCP chat, or run `mvn -f sample-maven/pom.xml test` in the terminal.
   - Show test output and the JaCoCo HTML report path (open `target/site/jacoco/index.html` if desired).

6. Iterate & commit (30–45s)
   - If coverage improved, show using `coverage_summary(dir="sample-maven")`.
   - Optionally show automated commit: `git_add_all()` followed by `git_commit("Add generated test", include_coverage=true)` and `git_push()`.

7. Wrap-up (10–20s)
   - Summarize what improved (coverage delta, tests added) and mention where to find the reflection PDF and source.

Recording tips
- Use a screen recorder (OBS, built-in OS recorder). Record at 720p or 1080p.
- Keep sections concise; use short commands and show results clearly.
- If you prefer, record narration after you record the screen (voice-over).

Files to attach when submitting
- `docs/reflection.pdf` (compile from `docs/reflection.tex`).
- A link to the recorded demo or upload the video (mp4).

Optional: sample terminal commands to run locally
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1
# Start server
python server.py
# In another shell run tests
mvn -f sample-maven/pom.xml test
```

End of demo script.
