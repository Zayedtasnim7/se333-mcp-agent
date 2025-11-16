"""Demo runner for SE333 MCP testing agent.

This script programmatically calls functions exported in `server.py` to exercise
an automated demo sequence suitable for recording:
 1. Get current coverage summary
 2. Find uncovered methods
 3. Generate a basic JUnit test for the first uncovered method (if any)
 4. Run mvn_test
 5. Show coverage summary again

Usage: run this from the repository root with the same Python environment that
has FastMCP and project dependencies installed (so that imports work).

Note: importing `server` will NOT start the MCP server because the module's
`app.run` call is guarded by `if __name__ == '__main__'`.
"""
import time
from pprint import pprint

import server


def main():
    proj = "sample-maven"
    print("1) Coverage summary (before)")
    cov = server.coverage_summary(proj)
    pprint(cov)

    print("\n2) Find uncovered methods")
    unc = server.find_uncovered_methods(proj)
    pprint(unc)

    if unc.get("count", 0) > 0 and unc.get("items"):
        target = unc["items"][0]
        cls = target["class"].split("/")[-1]
        method = target["method"]
        print(f"\n3) Generating basic JUnit for {cls}.{method}")
        res = server.generate_basic_junit(class_name=cls, method_name=method, dir=proj)
        pprint(res)
    else:
        print("No uncovered methods found; skipping test generation.")

    print("\n4) Running mvn_test")
    test_res = server.mvn_test(proj)
    pprint(test_res)

    print("\n5) Coverage summary (after)")
    cov2 = server.coverage_summary(proj)
    pprint(cov2)

    print("Done.")


if __name__ == "__main__":
    main()
