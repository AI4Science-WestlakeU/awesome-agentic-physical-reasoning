#!/usr/bin/env python3
"""Render the README tables and data/benchmarks.json from the YAML data.

Usage: python3 scripts/build_readme.py   (run from the repository root)
data/benchmarks.yaml  -> the audit tables between <!-- AUDIT:START --> and <!-- AUDIT:END -->, and data/benchmarks.json
data/out_of_scope.yaml -> the collapsed examples table between <!-- OUT_OF_SCOPE:START --> and <!-- OUT_OF_SCOPE:END -->
"""
import html
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "benchmarks.yaml"
OOS = ROOT / "data" / "out_of_scope.yaml"
README = ROOT / "README.md"
JSON_OUT = ROOT / "data" / "benchmarks.json"

CAPS = ["GDD", "PAP", "EE", "FE", "CLR"]
MARK = {"yes": "✓", "no": "✗", "partial": "◐", "unclear": "?"}
PHYSICS = {"symbolic", "simplified", "realistic", "partial"}
EVALUATION = {"goal-state", "functional", "answer", "judge", "mixed"}
STATUS = {"audited", "candidate"}
# The four classes of the paper (Section 3.2): the physics a benchmark employs and, under realistic physics, the task it poses.
CLASSES = [
    ("Construction", "realistic physics, building artifacts"),
    ("Embodied", "realistic physics, acting toward goals"),
    ("Simplified Sandbox", "simplified physics"),
    ("Symbolic-Physical", "symbolic state"),
]
KINDS = [
    ("no-physics-environment", "No interactive physics environment", "criterion 1 or 2"),
    ("no-text-interface", "No text-based interaction interface", "criterion 3"),
    ("not-a-benchmark", "Not evaluation suites", "methods and generators"),
]
COLS = 9


def esc(s):
    return html.escape(str(s), quote=True)


def name_cell(b, mark=""):
    """The name links to the paper; small text gives the year of first release and a code link."""
    name = f'<a href="{esc(b["paper"])}">{esc(b["name"])}</a>' if b.get("paper") else esc(b["name"])
    extra = [str(b["year"])]
    if b.get("code"):
        extra.append(f'<a href="{esc(b["code"])}">code</a>')
    return f'{name}{mark} <sub>{" · ".join(extra)}</sub>'


def row(b, mark=""):
    cells = [f"<td>{name_cell(b, mark)}</td>"]
    cells += [f'<td align="center">{MARK[b["capabilities"][c]]}</td>' for c in CAPS]
    cells += [f"<td>{esc(b['physics'])}</td>", f"<td>{esc(b['evaluation'])}</td>",
              f'<td align="center">{MARK[b["meets_standard"]]}</td>']
    return "<tr>" + "".join(cells) + "</tr>"


def group_row(title, detail="", span=COLS):
    label = f"<b>{esc(title)}</b>" + (f" · <sub>{esc(detail)}</sub>" if detail else "")
    return f'<tr><td colspan="{span}">{label}</td></tr>'


def table(items):
    head = ('<table>\n<thead><tr><th align="left">Benchmark</th>'
            + "".join(f'<th align="center">{c}</th>' for c in CAPS)
            + '<th align="left">Physics</th><th align="left">Evaluation</th><th align="center">Both</th></tr></thead>\n<tbody>')
    # Footnotes are numbered in the order of the records in the YAML, so a number stays with its record when rows move.
    noted = [b for b in items if b.get("footnote")]
    number = {id(b): i for i, b in enumerate(noted, 1)}
    lines, notes = [head], [b["footnote"] for b in noted]
    for cls, detail in CLASSES:
        group = [b for b in items if b["class"] == cls]
        if not group:
            continue
        lines.append(group_row(cls, detail))
        for b in sorted(group, key=lambda b: (-b["year"], b["name"])):
            # &#8288; is a word joiner: it keeps the mark on the same line as the end of the name
            mark = f"&#8288;<sup>[{number[id(b)]}]</sup>" if b.get("footnote") else ""
            lines.append(row(b, mark))
    lines.append("</tbody>\n</table>")
    if notes:
        lines += ["", "<details>", f"<summary><sub>Notes ({len(notes)})</sub></summary>", ""]
        lines += [f"<sub>[{i}] {n}</sub><br>" if i < len(notes) else f"<sub>[{i}] {n}</sub>" for i, n in enumerate(notes, 1)]
        lines += ["", "</details>"]
    return "\n".join(lines)


def norm(v):
    """YAML 1.1 reads yes/no as booleans; the audit wants the words."""
    return {True: "yes", False: "no"}.get(v, v)


def load_audit():
    items = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    named = {c for c, _ in CLASSES}
    for b in items:
        b["meets_standard"] = norm(b.get("meets_standard"))
        b["capabilities"] = {k: norm(v) for k, v in (b.get("capabilities") or {}).items()}
        b["in_paper"] = bool(b.get("in_paper", False))
        missing = [k for k in ("name", "status", "year", "class", "physics", "evaluation", "capabilities", "meets_standard", "assessed") if k not in b]
        if missing:
            sys.exit(f"{b.get('name', '?')}: missing {missing}")
        bad = [c for c in CAPS if b["capabilities"].get(c) not in MARK]
        if bad:
            sys.exit(f"{b['name']}: capability values must be yes/no/partial/unclear, got {bad}")
        if b["status"] not in STATUS:
            sys.exit(f"{b['name']}: status must be one of {sorted(STATUS)}")
        if b["physics"] not in PHYSICS or b["evaluation"] not in EVALUATION:
            sys.exit(f"{b['name']}: physics must be one of {sorted(PHYSICS)}, evaluation one of {sorted(EVALUATION)}")
        if b["class"] not in named:
            sys.exit(f"{b['name']}: class must be one of {sorted(named)}")
        if b["meets_standard"] not in {"yes", "no", "partial"}:
            sys.exit(f"{b['name']}: meets_standard must be yes/no/partial")
        if b["in_paper"] and b["status"] != "audited":
            sys.exit(f"{b['name']}: entries from the paper are audited")
    return items


def month(d):
    return d.strftime("%B %Y")


def paper_dates(paper):
    """First assessment of the paper's audit, and any record re-assessed after it (see the changelog)."""
    first = min(b["assessed"] for b in paper)
    later = sorted((b for b in paper if b["assessed"] > first), key=lambda b: b["name"])
    text = f"Assessed in {month(first)}"
    if later:
        text += "; " + ", ".join(f"{b['name']} re-assessed in {month(b['assessed'])}" for b in later)
    return text + "."


def audit_block(items):
    paper = [b for b in items if b["in_paper"]]
    added = [b for b in items if not b["in_paper"] and b["status"] == "audited"]
    candidates = [b for b in items if b["status"] == "candidate"]
    meet = lambda group: sum(b["meets_standard"] == "yes" for b in group)
    block = [
        f"**In the paper** (Table 2, {len(paper)} benchmarks, {meet(paper)} meet both requirements). {paper_dates(paper)}",
        "",
        table(paper),
    ]
    if added:
        block += [
            "",
            f"**Added after the paper** ({len(added)} benchmarks, {meet(added)} meet both requirements). "
            "Assessed from the published texts and reviewed by the paper's authors. The evidence for each judgment is in `data/benchmarks.yaml`.",
            "",
            table(added),
        ]
    if candidates:
        block += [
            "",
            f"**Candidates** ({len(candidates)}). Assessed from the published texts, pending review by the paper's authors. "
            "The evidence for each judgment is in `data/benchmarks.yaml`.",
            "",
            table(candidates),
        ]
    return block


def oos_block():
    items = yaml.safe_load(OOS.read_text(encoding="utf-8"))
    kinds = {k for k, _, _ in KINDS}
    for o in items:
        missing = [k for k in ("name", "year", "kind", "evaluates", "paper") if not o.get(k)]
        if missing:
            sys.exit(f"out of scope {o.get('name', '?')}: missing {missing}")
        if o["kind"] not in kinds:
            sys.exit(f"out of scope {o['name']}: kind must be one of {sorted(kinds)}")
    lines = [
        "<details>",
        "<summary><b>Out-of-scope examples</b> (not exhaustive)</summary>",
        "",
        "Related work outside the scope, grouped by the criterion it misses. Most examples come from Section 3.2 and Appendix B of the paper.",
        "",
        "<table>",
        '<thead><tr><th align="left">Example</th><th align="left">Year</th><th align="left">What it evaluates</th></tr></thead>',
        "<tbody>",
    ]
    for kind, title, detail in KINDS:
        group = sorted((o for o in items if o["kind"] == kind), key=lambda o: (-o["year"], o["name"]))
        if not group:
            continue
        lines.append(group_row(title, detail, span=3))
        lines += [f'<tr><td><a href="{esc(o["paper"])}">{esc(o["name"])}</a></td><td>{o["year"]}</td><td>{esc(o["evaluates"])}</td></tr>' for o in group]
    lines += ["</tbody>", "</table>"]
    lines += ["", "</details>"]
    return lines, len(items)


def splice(text, start, end, body):
    if start not in text or end not in text:
        sys.exit(f"README.md lacks the markers {start} {end}")
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    return pre + "\n".join([start] + body + [end]) + post


def main():
    items = load_audit()
    oos, n_oos = oos_block()
    text = README.read_text(encoding="utf-8")
    text = splice(text, "<!-- AUDIT:START -->", "<!-- AUDIT:END -->", audit_block(items))
    text = splice(text, "<!-- OUT_OF_SCOPE:START -->", "<!-- OUT_OF_SCOPE:END -->", oos)
    README.write_text(text, encoding="utf-8")
    JSON_OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    n_paper = sum(b["in_paper"] for b in items)
    n_cand = sum(b["status"] == "candidate" for b in items)
    print(f"README: {n_paper} in the paper, {len(items) - n_paper - n_cand} added and audited, {n_cand} candidates, "
          f"{n_oos} out-of-scope examples; wrote {JSON_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
