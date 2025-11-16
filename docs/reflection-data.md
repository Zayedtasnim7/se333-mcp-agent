# Project Metrics & Data

## 1. MCP Tools Implemented

Total MCP tools: 14

1. `list_java_methods(dir=".")`
2. `generate_basic_junit(class_name, method_name, dir="sample-maven")`
3. `mvn_test(dir="sample-maven")`
4. `mvn_coverage(dir="sample-maven")`
5. `parse_jacoco(xml_path="sample-maven/target/site/jacoco/jacoco.xml")`
6. `coverage_summary(dir="sample-maven")`
7. `git_status(dir=".")`
8. `git_add_all(dir=".")`
9. `git_commit(message, dir=".", include_coverage=False, coverage_dir="sample-maven")`
10. `git_push(remote="origin", branch=None, dir=".")`
11. `git_pull_request(...)`
12. `find_uncovered_methods(dir="sample-maven")`
13. `try_fix_known_bugs(dir="sample-maven")`
14. `iterate_coverage(dir="sample-maven", max_rounds=3)`

## 2. Coverage Statistics (sample-maven)

Latest JaCoCo run (Calc + CalcTest):

- Instruction Coverage: 100% (7/7)
- Line Coverage:        100% (2/2)
- Complexity Coverage:  100% (2/2)
- Method Coverage:      100% (2/2)
- Class Coverage:       100% (1/1)

If reporting before/after:
- Initial coverage: 0% (no tests for `Calc`)
- Final coverage:   100% after using the MCP testing agent
- Improvement:      +100 percentage points

## 3. Test Suite Summary

- Total test classes: 1
- Example: `CalcTest.java` (JUnit tests generated for `Calc`)

## 4. Git History Snapshot

Total commits (at metrics time): 12

Recent commits:
- c92b925 docs: add Quickstart to README
- 3f82148 docs: add Highlights to README
- f12bab3 chore: add CI badge to README
- c244cd4 chore: add CI badge to README
- 096f1b4 chore: add PR template

This shows the evolution from initial MCP server setup → coverage tooling → documentation & polish.