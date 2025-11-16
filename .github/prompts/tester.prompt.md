---
mode: "agent"
tools: [`mvn_coverage`, `mvn_test`, `generate_basic_junit`, `list_java_methods`, `coverage_summary`, `find_uncovered_methods`, `git_add_all`, `git_commit`, `git_push`, `git_pull_request`]
description: "Automated MCP testing agent for SE333 final project — generate, run, and iterate JUnit tests to maximize JaCoCo coverage."
model: 'Gpt-5 mini'
---

## Follow instruction below: ##
1. Run `coverage_summary(dir="sample-maven")` to collect current coverage (line & branch) and report paths.
2. Call `find_uncovered_methods(dir="sample-maven")` to list uncovered methods and select targets.
3. For each uncovered method, call `generate_basic_junit(class_name, method_name, dir="sample-maven")` to create a minimal JUnit 5 test.
4. Run `mvn_test(dir="sample-maven")` to execute tests. If tests fail, call `try_fix_known_bugs(dir="sample-maven")` (best-effort) and re-run `mvn_test` once.
5. When coverage increases meaningfully (e.g., any delta in line coverage), call `git_add_all(dir=".")` then `git_commit(message, include_coverage=True, coverage_dir="sample-maven")` and `git_push()`; optionally open a PR with `git_pull_request` (base: "main").
6. Always return a concise summary with: rounds performed, coverage before/after, tests created, any fixes applied, and PR URL if created.

Notes:
- Run Maven commands only inside the `sample-maven` folder.
- Keep edits minimal and add clear commit messages. Use `include_coverage=True` to include coverage stats in commit message.
- If external tools (mvn, git, gh) are missing, return an actionable error message describing how to install them.
