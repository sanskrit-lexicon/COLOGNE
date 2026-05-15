#!/usr/bin/env python3
"""Generate a non-destructive cleanup taxonomy proposal.

The script scans the repository and writes review-friendly files under
docs/cleanup/. It does not move, delete, or rewrite project files.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


LIFECYCLES = {
    "active-core": "Maintained code/data used by repeatable dictionary workflows.",
    "active-ops": "Maintained operational scripts or local setup helpers.",
    "generated-report": "Output that can probably be regenerated from scripts or data.",
    "reference-doc": "Human-facing documentation or scholarly/project reference material.",
    "legacy-python2": "Code that requires Python 2 or fails Python 3 syntax parsing.",
    "prototype": "Experimental API/frontend/export work that needs promotion or retirement.",
    "archival-issue": "Historical issue workspace; preserve for provenance by default.",
    "external-inventory": "Lists or notes about external services/artifacts.",
    "repo-governance": "Repository-level governance, contribution, or assistant metadata.",
}

WORKFLOWS = {
    "transliteration": "SLP1, IAST, Devanagari, or other transliteration mappings.",
    "xml-tag-audit": "XML-like tag counting and related generated tag reports.",
    "unicode-audit": "Extended Unicode/non-ASCII scans and reports.",
    "corrections": "Line-change or dictionary correction workflows.",
    "dictionary-export": "Markdown, StarDict, Babylon, or transform/export tooling.",
    "api-design": "API docs or service prototypes.",
    "frontend-prototype": "Browser-side prototype code or transformed HTML fixtures.",
    "local-install": "Local XAMPP/Mac setup, downloads, or environment notes.",
    "aws-inventory": "S3/AWS blob, scan, PDF, or listing references.",
    "issue-repair": "Issue-specific repair, analysis, or fixture material.",
    "scholarly-reference": "Bibliography, sandhi, presentation, or external reference files.",
    "repo-governance": "Repository metadata and contributor-facing process docs.",
    "review-roadmap": "Cleanup, architecture, or planning artifacts.",
}

ACTION_LABELS = {
    "keep-maintained": "Keep in place and maintain.",
    "test-and-package": "Add tests, package/import path, and keep active.",
    "mark-generated": "Mark as generated and document regeneration command.",
    "archive-no-refactor": "Preserve as historical material; do not refactor by default.",
    "port-or-retire": "Either port to Python 3/current tooling or explicitly retire.",
    "promote-or-sunset": "Decide whether to productize prototype or archive it.",
    "consolidate-shared": "Extract shared logic into a maintained module.",
    "harden-ops": "Improve safety, verification, paths, and failure handling.",
    "document-owner": "Assign maintainer/status and expected use.",
}

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".sh",
    ".xml",
    ".xsl",
    ".html",
    ".js",
    ".tsv",
    ".json",
    ".cff",
    ".gitignore",
    ".htaccess",
    ".diff",
    ".all",
}

EXCLUDED_DIRS = {".git", "__pycache__"}


@dataclass
class Proposal:
    path: str
    top_level: str
    kind: str
    lifecycle: str
    workflow: str
    proposed_action: str
    risk: str
    confidence: str
    duplicate_group: str
    rationale: str


def repo_files(root: Path, out_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve().is_relative_to(out_dir):
            continue
        parts = set(path.relative_to(root).parts)
        if parts & EXCLUDED_DIRS:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix().lower())


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def python3_syntax_error(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            ast.parse(source, filename=str(path))
    except SyntaxError as err:
        return f"SyntaxError: {err.msg}"
    except UnicodeDecodeError as err:
        return f"UnicodeDecodeError: {err}"
    return ""


def line_count(path: Path) -> int:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return 0
    try:
        with path.open("r", encoding="utf-8") as stream:
            return sum(1 for _ in stream)
    except UnicodeDecodeError:
        return 0


def classify(path: Path, root: Path, duplicate_group: str) -> Proposal:
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    top = parts[0]
    suffix = path.suffix.lower()
    name = path.name
    stem = path.stem
    kind = "binary-artifact" if suffix not in TEXT_EXTENSIONS and name not in TEXT_EXTENSIONS else "text"
    lifecycle = "reference-doc"
    workflow = "scholarly-reference"
    action = "document-owner"
    risk = "low"
    confidence = "medium"
    reasons: list[str] = []

    if suffix == ".py":
        kind = "python-script"
    elif suffix == ".sh":
        kind = "shell-script"
    elif suffix in {".md", ".txt"}:
        kind = "documentation-or-report"
    elif suffix in {".xml", ".xsl"}:
        kind = "xml-data"
    elif suffix in {".html", ".js"}:
        kind = "web-prototype"

    if top in {".ai_state.md", ".claude", ".gitignore", "README.md", "CLAUDE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "CITATION.cff"}:
        lifecycle = "repo-governance"
        workflow = "repo-governance"
        action = "keep-maintained"
        confidence = "high"
        reasons.append("repo-level governance or metadata")
    elif top == "ARCHITECTURE_REVIEW.md":
        lifecycle = "reference-doc"
        workflow = "review-roadmap"
        action = "keep-maintained"
        confidence = "high"
        reasons.append("cleanup/architecture planning artifact")
    elif top == "docs":
        lifecycle = "reference-doc"
        workflow = "review-roadmap"
        action = "keep-maintained"
        confidence = "high"
        reasons.append("cleanup documentation generated for review")
    elif top == "tools":
        lifecycle = "active-ops"
        workflow = "review-roadmap"
        action = "keep-maintained"
        confidence = "high"
        reasons.append("cleanup automation script")
    elif top == "api":
        lifecycle = "reference-doc"
        workflow = "api-design"
        action = "document-owner"
        confidence = "high"
        reasons.append("API design documentation")
    elif top == "aws":
        lifecycle = "external-inventory"
        workflow = "aws-inventory"
        action = "archive-no-refactor"
        confidence = "high"
        reasons.append("external AWS/blob inventory")
    elif top == "xmltag":
        workflow = "xml-tag-audit"
        if suffix in {".py", ".sh"} or name == "readme.txt":
            lifecycle = "active-core"
            action = "test-and-package" if suffix == ".py" else "harden-ops"
            confidence = "high"
            reasons.append("repeatable XML tag audit workflow")
        else:
            lifecycle = "generated-report"
            action = "mark-generated"
            confidence = "high"
            reasons.append("generated XML tag report")
    elif top == "eascii":
        workflow = "unicode-audit"
        if len(parts) > 1 and parts[1] in {"eadata", "eachanges-degree"}:
            lifecycle = "generated-report" if parts[1] == "eadata" else "archival-issue"
            action = "mark-generated" if parts[1] == "eadata" else "archive-no-refactor"
            confidence = "high"
            reasons.append("generated Unicode report or historical correction batch")
        elif suffix in {".py", ".sh"} or name == "readme.txt":
            lifecycle = "active-core"
            action = "test-and-package" if suffix == ".py" else "harden-ops"
            confidence = "high"
            reasons.append("repeatable Unicode audit workflow")
        else:
            lifecycle = "generated-report"
            action = "mark-generated"
            confidence = "high"
            reasons.append("generated Unicode summary")
    elif top == "iast":
        workflow = "transliteration"
        if suffix in {".py", ".xml"} or name == "readme.txt":
            lifecycle = "active-core"
            action = "test-and-package"
            risk = "high" if suffix == ".py" else "medium"
            confidence = "high"
            reasons.append("canonical transliteration mapping or validator")
        elif suffix == ".sh":
            lifecycle = "active-ops"
            action = "harden-ops"
            risk = "medium"
            confidence = "high"
            reasons.append("local install/update helper")
        else:
            lifecycle = "generated-report"
            action = "mark-generated"
            confidence = "high"
            reasons.append("generated transliteration report")
    elif top == "enhancements":
        if len(parts) > 1 and parts[1] == "code":
            workflow = "corrections"
            lifecycle = "active-core"
            action = "test-and-package" if suffix == ".py" else "harden-ops"
            confidence = "high"
            reasons.append("shared enhancement/correction utility")
            if name.endswith("_python2.py"):
                lifecycle = "legacy-python2"
                action = "port-or-retire"
                risk = "medium"
                reasons.append("explicit Python 2 variant")
            if name == "dictionary_init.sh":
                lifecycle = "active-ops"
                action = "harden-ops"
                risk = "high"
                reasons.append("downloads and unpacks external artifacts")
        else:
            workflow = "issue-repair"
            lifecycle = "prototype" if suffix == ".py" else "archival-issue"
            action = "promote-or-sunset" if suffix == ".py" else "archive-no-refactor"
            confidence = "medium"
            reasons.append("enhancement experiment outside shared code")
    elif top == "makemd":
        lifecycle = "active-core"
        workflow = "dictionary-export"
        action = "test-and-package"
        confidence = "high"
        reasons.append("Markdown export workflow")
    elif top == "stardict":
        lifecycle = "legacy-python2" if suffix == ".py" else "active-ops"
        workflow = "dictionary-export"
        action = "port-or-retire" if suffix == ".py" else "harden-ops"
        risk = "high" if suffix == ".py" else "medium"
        confidence = "high"
        reasons.append("legacy StarDict/Babylon export workflow")
        if name == "transcoder.py":
            action = "consolidate-shared"
            reasons.append("duplicate transliteration implementation")
    elif top == "localinstall":
        lifecycle = "active-ops"
        workflow = "local-install"
        action = "harden-ops"
        risk = "medium"
        confidence = "high"
        reasons.append("local installation/download helper")
    elif top == "issues":
        lifecycle = "archival-issue"
        workflow = "issue-repair"
        action = "archive-no-refactor"
        confidence = "high"
        reasons.append("issue-specific historical workspace")
        issue = parts[1] if len(parts) > 1 else ""
        if issue in {"issue445", "issue443", "issue441", "issue442"}:
            lifecycle = "prototype"
            workflow = "api-design" if issue == "issue445" else "frontend-prototype"
            action = "promote-or-sunset"
            risk = "high" if issue == "issue445" else "medium"
            reasons.append("prototype service/frontend/export experiment")
    elif top == "misc":
        lifecycle = "reference-doc"
        workflow = "scholarly-reference"
        action = "archive-no-refactor"
        confidence = "high"
        reasons.append("miscellaneous scholarly/reference artifact")
    elif top == "xsswork":
        lifecycle = "reference-doc"
        workflow = "api-design"
        action = "document-owner"
        risk = "high"
        confidence = "high"
        reasons.append("security remediation notes")

    if suffix == ".py":
        syntax_error = python3_syntax_error(path)
        if syntax_error:
            lifecycle = "legacy-python2"
            action = "port-or-retire"
            risk = "high"
            reasons.append(syntax_error)

    if duplicate_group and suffix == ".py" and lifecycle not in {"legacy-python2"}:
        if lifecycle == "archival-issue":
            reasons.append(f"duplicate Python file in {duplicate_group}; leave archival copy unless migrating future work")
        else:
            action = "consolidate-shared"
            risk = "medium"
            reasons.append(f"duplicate Python file in {duplicate_group}")

    if suffix in {".pdf", ".doc", ".pptx"}:
        kind = "reference-artifact"
        lifecycle = "reference-doc"
        workflow = "scholarly-reference"
        action = "archive-no-refactor"
        confidence = "high"
        reasons.append("binary scholarly/reference artifact")

    return Proposal(
        path=rel,
        top_level=top,
        kind=kind,
        lifecycle=lifecycle,
        workflow=workflow,
        proposed_action=action,
        risk=risk,
        confidence=confidence,
        duplicate_group=duplicate_group,
        rationale="; ".join(reasons) if reasons else "heuristic classification",
    )


def duplicate_groups(files: list[Path]) -> dict[Path, str]:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        by_hash[file_sha(path)].append(path)

    groups: dict[Path, str] = {}
    index = 1
    for paths in sorted(by_hash.values(), key=lambda p: (-len(p), p[0].as_posix())):
        if len(paths) < 2:
            continue
        group_name = f"dup-{index:03d}"
        for path in paths:
            groups[path] = group_name
        index += 1
    return groups


def write_schema(out_dir: Path) -> None:
    lines = [
        "# Cleanup Taxonomy Schema",
        "",
        "This taxonomy is a proposal layer. It is intended for human approval before any file moves, deletes, or refactors.",
        "",
        "## Lifecycle Labels",
        "",
    ]
    for key, value in LIFECYCLES.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Workflow Labels", ""])
    for key, value in WORKFLOWS.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Proposed Actions", ""])
    for key, value in ACTION_LABELS.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Approval Columns",
            "",
            "The generated CSV leaves `human_decision` and `human_notes` blank. Suggested values for `human_decision`:",
            "",
            "- `approve`: accept the proposed taxonomy/action.",
            "- `override`: keep the path but change lifecycle, workflow, or action.",
            "- `defer`: revisit after related cleanup issues land.",
            "- `ignore`: exclude from cleanup tracking.",
            "",
        ]
    )
    (out_dir / "taxonomy_schema.md").write_text("\n".join(lines), encoding="utf-8")


def write_csv(out_dir: Path, proposals: list[Proposal]) -> None:
    fieldnames = [
        "path",
        "top_level",
        "kind",
        "lifecycle",
        "workflow",
        "proposed_action",
        "risk",
        "confidence",
        "duplicate_group",
        "rationale",
        "human_decision",
        "human_notes",
    ]
    with (out_dir / "taxonomy_proposals.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for proposal in proposals:
            row = proposal.__dict__.copy()
            row["human_decision"] = ""
            row["human_notes"] = ""
            writer.writerow(row)


def write_summary(out_dir: Path, proposals: list[Proposal]) -> None:
    lifecycle_counts = Counter(p.lifecycle for p in proposals)
    workflow_counts = Counter(p.workflow for p in proposals)
    action_counts = Counter(p.proposed_action for p in proposals)
    risk_counts = Counter(p.risk for p in proposals)

    by_top: dict[str, list[Proposal]] = defaultdict(list)
    for proposal in proposals:
        by_top[proposal.top_level].append(proposal)

    lines = [
        "# Cleanup Taxonomy Proposal",
        "",
        "Generated by `tools/propose_cleanup_taxonomy.py`.",
        "",
        "This is a non-destructive approval list. It proposes how to label and handle project areas before any cleanup changes are made.",
        "",
        "## Counts",
        "",
        f"- Files scanned: {len(proposals)}",
        f"- Lifecycle labels: {', '.join(f'{k}={v}' for k, v in sorted(lifecycle_counts.items()))}",
        f"- Risk labels: {', '.join(f'{k}={v}' for k, v in sorted(risk_counts.items()))}",
        "",
        "## Proposed Directory Taxonomy",
        "",
        "| Area | Primary lifecycle | Primary workflow | Primary action | Files | Notes |",
        "|---|---|---|---|---:|---|",
    ]

    for top, items in sorted(by_top.items()):
        lifecycle = Counter(p.lifecycle for p in items).most_common(1)[0][0]
        workflow = Counter(p.workflow for p in items).most_common(1)[0][0]
        action = Counter(p.proposed_action for p in items).most_common(1)[0][0]
        notes = Counter(p.rationale for p in items).most_common(1)[0][0]
        notes = notes.replace("|", "\\|")
        lines.append(f"| `{top}` | `{lifecycle}` | `{workflow}` | `{action}` | {len(items)} | {notes} |")

    lines.extend(["", "## Lifecycle Totals", ""])
    for key, count in sorted(lifecycle_counts.items()):
        lines.append(f"- `{key}`: {count}")

    lines.extend(["", "## Workflow Totals", ""])
    for key, count in sorted(workflow_counts.items()):
        lines.append(f"- `{key}`: {count}")

    lines.extend(["", "## Proposed Action Totals", ""])
    for key, count in sorted(action_counts.items()):
        lines.append(f"- `{key}`: {count}")

    lines.extend(
        [
            "",
            "## Human Approval Queue",
            "",
            "Start with high-risk or high-leverage areas before approving bulk archival labels.",
            "",
            "| Priority | Paths | Proposed action | Reason |",
            "|---:|---|---|---|",
        ]
    )

    priority_rows = [
        ("1", "`iast/transcoder.py`, `iast/*.xml`, `stardict/transcoder.py`", "`consolidate-shared` / `test-and-package`", "Transliteration should become one reliable shared source."),
        ("2", "`enhancements/code/updateByLine.py`, copied issue `updateByLine.py` files", "`test-and-package` / `archive-no-refactor`", "Correction application is core, but historical copies should not drive future edits."),
        ("3", "`stardict/make_babylon.py`, `enhancements/issue10/*.py`", "`port-or-retire`", "These fail Python 3 syntax checks."),
        ("4", "`issues/issue445/`", "`promote-or-sunset`", "API/frontend prototype needs a product decision before hardening."),
        ("5", "`xmltag/`, `eascii/` generated reports", "`mark-generated`", "Generated output should be labeled before moving or regenerating."),
        ("6", "`localinstall/`, `enhancements/code/dictionary_init.sh`", "`harden-ops`", "Download/setup workflows need safer defaults and explicit paths."),
    ]
    for row in priority_rows:
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")

    lines.extend(
        [
            "",
            "## Approval Workflow",
            "",
            "1. Review `taxonomy_schema.md` and adjust labels if needed.",
            "2. Review `taxonomy_proposals.csv`; fill `human_decision` and `human_notes`.",
            "3. Approve high-risk areas individually before approving generated reports or archival issue folders in bulk.",
            "4. Use approved rows to create follow-up cleanup issues; do not move files directly from this proposal.",
            "",
        ]
    )

    (out_dir / "taxonomy_summary.md").write_text("\n".join(lines), encoding="utf-8")


def write_issue_backlog(out_dir: Path, proposals: list[Proposal]) -> None:
    counts_by_action = Counter(p.proposed_action for p in proposals)
    counts_by_lifecycle = Counter(p.lifecycle for p in proposals)

    issues = [
        {
            "title": "Approve cleanup taxonomy schema and inventory workflow",
            "labels": "cleanup, governance, approval",
            "slice": "`taxonomy_schema.md`, `taxonomy_summary.md`, `taxonomy_proposals.csv`",
            "scope": "Approve lifecycle, workflow, action, risk, and human decision labels before any cleanup operations.",
            "approval": "Are the labels sufficient, and should the CSV be the source of truth for cleanup approvals?",
            "count": len(proposals),
        },
        {
            "title": "Mark generated reports and document regeneration commands",
            "labels": "cleanup, generated, documentation",
            "slice": "`xmltag/xmltag_*.txt`, `xmltag/all_xmltags.txt`, `eascii/eadata/*`, `eascii/easummary*.tsv`",
            "scope": "Classify generated report files and add regeneration commands before changing storage policy.",
            "approval": "Which generated reports should remain committed, and which can be regenerated on demand?",
            "count": counts_by_action["mark-generated"],
        },
        {
            "title": "Preserve issue workspaces as archival by default",
            "labels": "cleanup, archival, issues",
            "slice": "`issues/**` except explicitly promoted prototypes or shared-code migration candidates",
            "scope": "Approve `archive-no-refactor` for historical issue directories so future cleanup does not rewrite provenance.",
            "approval": "Which issue directories, if any, are still active and should be removed from archival handling?",
            "count": counts_by_lifecycle["archival-issue"],
        },
        {
            "title": "Package and test active core scripts",
            "labels": "cleanup, testing, active-core",
            "slice": "`iast/`, `xmltag/*.py`, `eascii/*.py`, `enhancements/code/*.py`, `makemd/make_md.py`",
            "scope": "Add fixtures and tests around active behavior before refactoring imports or paths.",
            "approval": "Are these the right active core workflows to support first?",
            "count": counts_by_lifecycle["active-core"],
        },
        {
            "title": "Consolidate transliteration into one maintained source",
            "labels": "cleanup, transliteration, architecture",
            "slice": "`iast/transcoder.py`, `iast/*.xml`, `stardict/transcoder.py`",
            "scope": "Fix lookup behavior, fail loudly on missing XML, and remove divergent transcoder copies from active workflows.",
            "approval": "Should `iast/` become the canonical Python transliteration source?",
            "count": 3,
        },
        {
            "title": "Decide port-or-retire policy for Python 2 and legacy scripts",
            "labels": "cleanup, python2, legacy",
            "slice": "`stardict/make_babylon.py`, `enhancements/code/updateByLine_python2.py`, `enhancements/issue10/*.py`",
            "scope": "Either port scripts to supported Python or mark them as retired/archival with clear docs.",
            "approval": "Which legacy workflows are still needed by maintainers?",
            "count": counts_by_lifecycle["legacy-python2"],
        },
        {
            "title": "Promote or sunset prototypes",
            "labels": "cleanup, prototype, decision",
            "slice": "`issues/issue445/`, `issues/issue443/`, `issues/issue441/`, `issues/issue442/`",
            "scope": "Decide whether API/frontend/export prototypes become maintained projects or remain archival experiments.",
            "approval": "Which prototypes should receive hardening work?",
            "count": counts_by_lifecycle["prototype"],
        },
        {
            "title": "Harden operational setup and download workflows",
            "labels": "cleanup, ops, security",
            "slice": "`localinstall/**`, `enhancements/code/dictionary_init.sh`, batch `redo_*.sh` scripts",
            "scope": "Add explicit paths, HTTPS/fail-fast downloads, verification, and clearer operational docs.",
            "approval": "Which local install/download workflows are still used?",
            "count": counts_by_action["harden-ops"],
        },
        {
            "title": "Assign owners for reference and governance material",
            "labels": "cleanup, docs, ownership",
            "slice": "`api/`, `aws/`, `misc/`, root reference files, `xsswork/`",
            "scope": "Clarify what should stay as reference, what is external inventory, and who owns updates.",
            "approval": "Which reference materials are canonical, historical, or obsolete?",
            "count": counts_by_action["document-owner"] + counts_by_lifecycle["reference-doc"] + counts_by_lifecycle["external-inventory"],
        },
    ]

    lines = [
        "# Proposed Cleanup Issue Backlog",
        "",
        "Generated by `tools/propose_cleanup_taxonomy.py`.",
        "",
        "Each item is an approval slice. A human should approve, override, split, or reject these before implementation begins.",
        "",
    ]

    for index, issue in enumerate(issues, start=1):
        lines.extend(
            [
                f"## {index}. {issue['title']}",
                "",
                f"- Labels: `{issue['labels']}`",
                f"- Approximate affected rows: {issue['count']}",
                f"- Taxonomy slice: {issue['slice']}",
                f"- Scope: {issue['scope']}",
                f"- Human approval question: {issue['approval']}",
                "",
            ]
        )

    (out_dir / "cleanup_issue_backlog.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate cleanup taxonomy proposals.")
    parser.add_argument("--root", default=".", help="Repository root to scan.")
    parser.add_argument("--out-dir", default="docs/cleanup", help="Output directory for generated proposals.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_dir = (root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    files = repo_files(root, out_dir)
    duplicates = duplicate_groups(files)
    proposals = [classify(path, root, duplicates.get(path, "")) for path in files]

    write_schema(out_dir)
    write_csv(out_dir, proposals)
    write_summary(out_dir, proposals)
    write_issue_backlog(out_dir, proposals)

    print(f"Wrote {len(proposals)} proposals to {out_dir}")
    print(f"- {out_dir / 'taxonomy_schema.md'}")
    print(f"- {out_dir / 'taxonomy_summary.md'}")
    print(f"- {out_dir / 'taxonomy_proposals.csv'}")
    print(f"- {out_dir / 'cleanup_issue_backlog.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
