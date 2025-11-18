# SE333 MCP Testing Agent

**Author:** Tasnim Zayed  
**Course:** SE333 - Software Agents  
**Date:** November 17th 2025

## 📺 Demo Video

**Location:** `demo/final_presentation.mp4` (35.2 MB, 4 minutes 15 seconds)

*Note: The video file may be too large to preview directly in GitHub. Please download it to view.*

**To download:**
1. Navigate to [`demo/final_presentation.mp4`](./demo/final_presentation.mp4)
2. Click the "Download" button
3. Open the downloaded file on your computer

## 📄 Reflection Report

**Location:** `report/reflection.pdf` (119 KB, 4 pages)

The reflection report includes:
- Project overview and objectives
- Methodology and implementation details
- Coverage results and metrics
- Challenges and solutions
- Lessons learned

**View online:** [report/reflection.pdf](./report/reflection.pdf)

---

## 🎯 Project Overview

This project implements an intelligent testing agent using the Model Context Protocol (MCP) that automatically generates JUnit tests, measures code coverage, and automates Git workflows - all from within VS Code.

### Key Achievements:
- ✅ **14 MCP tools** implemented for automated testing and Git operations
- ✅ **100% test coverage** achieved (instruction, line, method, class)
- ✅ **Automated workflow** from test generation to version control
- ✅ **VS Code integration** for seamless developer experience

---

## 🛠️ MCP Tools Implemented

### Test & Coverage Tools (8 tools)
- `list_java_methods` - Scan Java files for methods to test
- `generate_basic_junit` - Generate JUnit test skeletons
- `mvn_test` - Run Maven tests
- `mvn_coverage` - Generate JaCoCo coverage report
- `parse_jacoco` - Parse JaCoCo XML results
- `coverage_summary` - Summarize coverage metrics
- `find_uncovered_methods` - Identify gaps in coverage
- `iterate_coverage` - Iteratively improve coverage

### Git Automation Tools (5 tools)
- `git_status` - Check repository status
- `git_add_all` - Stage all changes
- `git_commit` - Create commits with messages
- `git_push` - Push to remote repository
- `git_pull_request` - Create pull requests

### Utilities (1 tool)
- `try_fix_known_bugs` - Auto-fix common issues

---

## 📊 Coverage Results

**Initial State:** 0% coverage  
**Final State:** 100% coverage across all metrics

| Metric | Coverage | Details |
|--------|----------|---------|
| **Instruction** | 100% | 7/7 |
| **Line** | 100% | 2/2 |
| **Complexity** | 100% | 2/2 |
| **Method** | 100% | 2/2 |
| **Class** | 100% | 1/1 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Java 11+
- Maven 3.6+
- VS Code (latest version)

### Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/Zayedtasnim7/se333-mcp-agent.git
   cd se333-mcp-agent
```

2. **Set up Python environment:**
```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source .venv/bin/activate
   
   # Install dependencies
   pip install mcp[cli] httpx fastmcp
```

3. **Start the MCP server:**
```bash
   python server.py
```
   
   The server will start at: `http://127.0.0.1:6060/mcp`

4. **Connect to VS Code:**
   - Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
   - Search for "MCP: Add Server"
   - Enter URL: `http://127.0.0.1:6060/mcp`
   - Name it: "Testing Agent"
   - Press Enter

5. **Verify setup:**
   - Open VS Code Chat panel
   - You should see all 14 MCP tools listed
   - Test with: "List Java methods in sample-maven"

---

## 🧪 Running Tests

### Run tests manually:
```bash
cd sample-maven
mvn clean test
mvn jacoco:report
```

### View coverage report:
```bash
# Windows
start target\site\jacoco\index.html

# Mac/Linux
open target/site/jacoco/index.html
```

### Using the MCP agent:
In VS Code Chat:
```
Generate tests for Calc.java and run coverage analysis
```

---

## 📁 Project Structure
```
se333-mcp-agent/
├── server.py                      # MCP server (14 tools)
├── get_my_metrics.py              # Metrics collection script
├── show_metrics.py                # Metrics display script
├── README.md                      # This file
├── demo/
│   └── final_presentation.mp4     # Demo video (4:15)
├── report/
│   ├── reflection.pdf             # Reflection report (4 pages)
│   └── reflection.tex             # LaTeX source
├── docs/
│   ├── screenshots/               # 6 demo screenshots
│   │   ├── 1.png                 # MCP tools list
│   │   ├── 2.png                 # Generated tests
│   │   ├── 3.png                 # Coverage overview
│   │   ├── 4.png                 # Coverage details
│   │   ├── 5.png                 # Git automation
│   │   └── 6.png                 # VS Code workflow
│   └── my_project_metrics.txt     # Project metrics
├── .github/
│   └── prompts/
│       └── tester.prompt.md       # Agent prompt configuration
└── sample-maven/
    ├── pom.xml                    # Maven config with JaCoCo
    └── src/
        ├── main/java/             # Source code (Calc.java)
        └── test/java/             # Generated tests (CalcTest.java)
```

---

## 🎨 Screenshots

All screenshots are located in `docs/screenshots/`:

1. **MCP Tools List** (`1.png`) - Shows all 14 implemented tools
2. **Generated Tests** (`2.png`) - JUnit tests created by the agent
3. **Coverage Overview** (`3.png`) - JaCoCo report showing 100% coverage
4. **Coverage Details** (`4.png`) - Line-by-line coverage visualization
5. **Git Automation** (`5.png`) - Git commands executed by the agent
6. **VS Code Workflow** (`6.png`) - Complete development environment

---

## 💻 Usage Examples

### Example 1: Generate Tests
```
In VS Code Chat:
"Generate JUnit tests for the Calc class"
```

### Example 2: Check Coverage
```
In VS Code Chat:
"Analyze current test coverage for sample-maven"
```

### Example 3: Iterate to Improve Coverage
```
In VS Code Chat:
"Improve test coverage by generating tests for uncovered methods"
```

### Example 4: Git Automation
```
In VS Code Chat:
"Check git status, commit changes with message 'Add tests', and push to GitHub"
```

---

## 🔧 Troubleshooting

### Issue: "Site can't be reached" when opening MCP URL
**Solution:** This is normal. The MCP server is not a website - it's an API endpoint for VS Code to connect to. Use the "MCP: Add Server" command in VS Code instead.

### Issue: Maven tests fail
**Solution:** 
```bash
# Verify Java version (should be 11+)
java -version

# Clean and rebuild
cd sample-maven
mvn clean install
```

### Issue: MCP tools not showing in VS Code
**Solution:**
1. Verify server is running: `python server.py`
2. Restart VS Code
3. Re-add the server using "MCP: Add Server"

### Issue: Coverage report not generated
**Solution:**
```bash
cd sample-maven
mvn clean test jacoco:report
```

---

## 📚 Documentation

- **Reflection Report:** [`report/reflection.pdf`](./report/reflection.pdf)
- **Demo Video:** [`demo/final_presentation.mp4`](./demo/final_presentation.mp4)
- **Agent Prompt:** [`.github/prompts/tester.prompt.md`](./.github/prompts/tester.prompt.md)
- **Project Metrics:** [`docs/my_project_metrics.txt`](./docs/my_project_metrics.txt)

---

## 🎓 Assignment Requirements Met

✅ **Phase 1:** Environment setup and MCP integration  
✅ **Phase 2:** Core testing agent with Maven and JaCoCo  
✅ **Phase 3:** Git automation tools (5 tools)  
✅ **Phase 4:** Intelligent test iteration and coverage improvement  
✅ **Phase 5:** Creative extensions and advanced features  
✅ **Documentation:** Complete README, reflection report, and demo video  
✅ **Demo:** 4+ minute video demonstration  

---

## 🏆 Key Results

- **Coverage Improvement:** 0% → 100% (automated)
- **Test Files Generated:** CalcTest.java with 5 test methods
- **MCP Tools:** 14 fully functional tools
- **Git Commits:** 15+ commits showing iterative development
- **Lines of Code:** 450+ lines in server.py

---

## 🔮 Future Enhancements

- Support for mutation testing (PIT)
- Integration with additional testing frameworks (TestNG, Mockito)
- Support for mock object generation
- Enhanced AI-driven test case generation based on code analysis
- Integration with CI/CD pipelines
- Support for multi-module Maven projects

---

## 📝 License

This project was created for SE333 - Software Agents course assignment.

---

## 👤 Author

**Tasnim Zayed**  
GitHub: [@Zayedtasnim7](https://github.com/Zayedtasnim7)  
Repository: [se333-mcp-agent](https://github.com/Zayedtasnim7/se333-mcp-agent)

---

## 🙏 Acknowledgments

- SE333 Course Staff
- Anthropic's Claude AI for development assistance
- FastMCP framework
- JaCoCo for coverage analysis
- Maven for build automation

---

**Last Updated:** November 17, 2025