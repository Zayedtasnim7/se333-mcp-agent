"""
Simple generator: populate a LaTeX IEEE-style reflection.tex using
`docs/reflection-data.md` and `docs/my_project_metrics.txt`.

Usage:
    python build_reflection_tex.py --data docs/reflection-data.md --metrics docs/my_project_metrics.txt --out report/reflection.tex

This script is intentionally small and has no external dependencies.
"""
import argparse
import os
import re

TEX_HEADER = r"""% Auto-generated reflection.tex (IEEEtran)
\documentclass[conference]{IEEEtran}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\begin{document}
\title{Reflection Report: MCP Testing Agent}
\author{Your Name}
\maketitle
"""

TEX_FOOTER = r"""
\end{document}
"""

def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def md_to_latex(md: str) -> str:
    # Very small converter for headings, code spans, lists and paragraphs
    lines = md.splitlines()
    out = []
    for line in lines:
        if line.startswith('# '):
            out.append('\n\\section{' + line[2:].strip() + '}\n')
        elif line.startswith('## '):
            out.append('\n\\subsection{' + line[3:].strip() + '}\n')
        elif re.match(r'^- `.+`', line.strip()):
            # list item with code
            item = line.strip()[2:]
            out.append('\\paragraph{}\\texttt{' + item.strip(' -') + '}\\\\')
        elif line.startswith('- '):
            out.append('\\item ' + line[2:].strip())
        elif line.strip().startswith('1.') or re.match(r'^\d+\.', line.strip()):
            out.append(line)
        elif line.strip() == '':
            out.append('')
        else:
            # escape underscores
            s = line.replace('_', '\\_')
            out.append(s + '\\')
    # Join and wrap list items
    text = '\n'.join(out)
    # Convert simple lists beginning with \item into itemize env
    if '\\item' in text:
        parts = text.split('\n')
        in_list = False
        final = []
        for p in parts:
            if p.startswith('\\item') and not in_list:
                final.append('\\begin{itemize}')
                in_list = True
            final.append(p)
            if in_list and p == '':
                final.append('\\end{itemize}')
                in_list = False
        text = '\n'.join(final)
    return text


def generate_tex(data_md: str, metrics_txt: str) -> str:
    dmd = load_text(data_md)
    mtxt = load_text(metrics_txt)

    # Extract summary fields from reflection-data.md using simple regexes
    # We'll capture the Coverage Statistics block and MCP Tools list
    coverage_block = ''
    mcp_tools_block = ''

    # Find '## 1. MCP Tools Implemented' to next header
    m = re.search(r'## 1\. MCP Tools Implemented\n(.*?)\n##', dmd, re.S)
    if m:
        mcp_tools_block = m.group(1).strip()
    else:
        # fallback: take first 200 chars
        mcp_tools_block = dmd[:200]

    m = re.search(r'## 2\. Coverage Statistics \(sample-maven\)\n(.*?)\n##', dmd, re.S)
    if m:
        coverage_block = m.group(1).strip()
    else:
        coverage_block = ''

    # Basic LaTeX content
    body = []
    body.append(TEX_HEADER)

    # Abstract placeholder
    body.append('\\begin{abstract}\\small')
    body.append('This reflection summarizes the MCP testing agent, the coverage improvements achieved, and lessons learned from AI-assisted development.')
    body.append('\\end{abstract}')

    # Introduction from reflection-data.md first paragraph
    body.append('\\section{Introduction}')
    intro = dmd.splitlines()
    para = ''
    for line in intro:
        if line.strip():
            para = line.strip()
            break
    body.append(para + '\\')

    # Methodology
    body.append('\\section{Methodology}')
    body.append('The MCP agent was used to:')
    body.append('\\begin{itemize}')
    # list tools
    tools_lines = mcp_tools_block.splitlines()
    for t in tools_lines:
        t = t.strip()
        if t:
            # Clean numbering
            t = re.sub(r'^\d+\.', '', t).strip()
            body.append('\\item \texttt{' + t.replace('`','') + '}')
    body.append('\\end{itemize}')

    # Results & Discussion
    body.append('\\section{Results and Discussion}')
    body.append('\\subsection{Coverage Summary}')
    # Insert cleaned coverage summary
    if coverage_block:
        cov_lines = coverage_block.splitlines()
        body.append('\\begin{itemize}')
        for cl in cov_lines:
            cl = cl.strip()
            if cl.startswith('- '):
                body.append('\\item ' + cl[2:])
        body.append('\\end{itemize}')
    else:
        # fallback: include metrics text excerpt
        body.append('See attached metrics:')
        excerpt = '\\newline '.join(mtxt.splitlines()[:12])
        body.append('\\texttt{' + excerpt.replace('%','\\%') + '}')

    # AI-assisted development insights
    body.append('\\subsection{AI-assisted Development}')
    body.append('The agent generated tests and automated coverage iterations; the main insight was that AI helps find trivial unit tests but required manual guidance for edge cases.')

    # Challenges and Lessons
    body.append('\\section{Challenges and Lessons Learned}')
    body.append('Key challenges included configuring JaCoCo reporting, handling encoding differences on Windows, and iterating prompts to produce reliable tests.')

    # Recommendations
    body.append('\\section{Recommendations}')
    body.append('Future work: extend the agent to handle multi-module projects, add mutation testing (PIT), and automate PDF compilation in CI when TeX is available.')

    body.append(TEX_FOOTER)
    return '\n'.join(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='docs/reflection-data.md')
    parser.add_argument('--metrics', default='docs/my_project_metrics.txt')
    parser.add_argument('--out', default='report/reflection.tex')
    args = parser.parse_args()

    if not os.path.exists(args.data):
        print('ERROR: reflection data not found at', args.data)
        return 2
    if not os.path.exists(args.metrics):
        print('ERROR: metrics file not found at', args.metrics)
        return 2

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    tex = generate_tex(args.data, args.metrics)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(tex)
    print('Wrote', args.out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
