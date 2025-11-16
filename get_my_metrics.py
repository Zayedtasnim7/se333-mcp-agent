import xml.etree.ElementTree as ET
import subprocess, os

print("=" * 60)
print("PROJECT METRICS FOR REFLECTION")
print("=" * 60)

# MCP Tools count
print("\nMCP TOOLS COUNT:")
with open('server.py', 'r', encoding='utf-8') as f:
    count = f.read().count('@app.tool')
print(f"   Total Tools: {count}")

# Coverage
print("\nCOVERAGE STATISTICS:")
tree = ET.parse('sample-maven/target/site/jacoco/jacoco.xml')
root = tree.getroot()
for counter in root.findall('.//counter'):
    t = counter.get('type')
    missed = int(counter.get('missed'))
    covered = int(counter.get('covered'))
    total = missed + covered
    if total > 0:
        pct = (covered / total) * 100
        print(f"   {t}: {pct:.1f}% ({covered}/{total})")

# Test files
print("\nTEST FILES:")
# Modified for Windows
test_dir = 'sample-maven/src/test'
test_files = []
for root, dirs, files in os.walk(test_dir):
    for file in files:
        if file.endswith('Test.java'):
            test_files.append(os.path.join(root, file))

print(f"   Total Test Classes: {len(test_files)}")
for f in test_files:
    print("  ", os.path.basename(f))

# Git commits
print("\nGIT COMMITS:")
log = subprocess.run(['git', 'log', '--oneline'], capture_output=True, text=True)
commits = log.stdout.strip().split('\n')
print(f"   Total Commits: {len(commits)}")
for c in commits[:5]:
    print("   ", c)

print("\n" + "=" * 60)
print("SAVE THIS OUTPUT FOR YOUR REFLECTION")
print("=" * 60)