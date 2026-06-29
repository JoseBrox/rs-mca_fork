#!/usr/bin/env python3
"""Audit Markdown script-path references against actual repository paths.

Proof status: AUDIT. This deterministic scanner finds references such as
`experimental/foo.py` or `scripts/foo.py`, checks whether they exist, and, when
they do not, suggests actual script files with the same basename. It is meant to
separate genuinely missing computational targets from artifacts that were moved
under `experimental/scripts/`.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_RE = re.compile(
    r"(?P<path>(?:experimental|scripts)/[A-Za-z0-9_./-]+\.py)"
)
DEFAULT_MARKDOWN_GLOBS = (
    "agents.md",
    "readme.md",
    "experimental/README.md",
    "experimental/scripts/README.md",
    "experimental/notes/**/*.md",
)
SCRIPT_GLOBS = (
    "scripts/**/*.py",
    "experimental/scripts/**/*.py",
    "experimental/notes/certificate_scanner/**/*.py",
)


@dataclass(frozen=True)
class Reference:
    file: str
    line: int
    reference: str
    exists: bool
    candidates: list[str]
    historical: bool


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def existing_script_paths() -> set[str]:
    paths: set[str] = set()
    for pattern in SCRIPT_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file():
                paths.add(relative(path))
    return paths


def candidate_map(scripts: set[str]) -> dict[str, list[str]]:
    by_name: dict[str, list[str]] = {}
    for path in sorted(scripts):
        by_name.setdefault(Path(path).name, []).append(path)
    return by_name


def markdown_files(include_triage: bool) -> list[Path]:
    files: set[Path] = set()
    for pattern in DEFAULT_MARKDOWN_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = relative(path)
            if not include_triage and rel.startswith("experimental/notes/triage/"):
                continue
            files.add(path)
    return sorted(files)


def scan_file(path: Path, scripts: set[str], by_name: dict[str, list[str]]) -> list[Reference]:
    rel_file = relative(path)
    historical = rel_file.startswith("experimental/notes/triage/")
    refs: list[Reference] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in REFERENCE_RE.finditer(line):
            ref = match.group("path")
            exists = ref in scripts or (REPO_ROOT / ref).is_file()
            candidates = [] if exists else by_name.get(Path(ref).name, [])
            refs.append(
                Reference(
                    file=rel_file,
                    line=line_number,
                    reference=ref,
                    exists=exists,
                    candidates=candidates,
                    historical=historical,
                )
            )
    return refs


def build_report(include_triage: bool) -> dict[str, Any]:
    scripts = existing_script_paths()
    by_name = candidate_map(scripts)
    references = [
        ref
        for path in markdown_files(include_triage)
        for ref in scan_file(path, scripts, by_name)
    ]
    stale = [ref for ref in references if not ref.exists and ref.candidates]
    missing = [ref for ref in references if not ref.exists and not ref.candidates]

    return {
        "metadata": {
            "proof_status": "AUDIT",
            "theorem_problem_id": "script-path-reference-audit",
            "determinism": "deterministic source scan; no random seed",
            "include_triage": include_triage,
            "markdown_globs": list(DEFAULT_MARKDOWN_GLOBS),
            "script_globs": list(SCRIPT_GLOBS),
        },
        "result": {
            "audit_result": "REVIEW" if stale or missing else "PASS",
            "references": len(references),
            "existing_references": len([ref for ref in references if ref.exists]),
            "stale_references_with_candidates": len(stale),
            "missing_references_without_candidates": len(missing),
        },
        "stale_references_with_candidates": [asdict(ref) for ref in stale],
        "missing_references_without_candidates": [asdict(ref) for ref in missing],
    }


def format_text(report: dict[str, Any]) -> str:
    meta = report["metadata"]
    result = report["result"]
    lines = [
        "Script path reference audit",
        f"proof_status: {meta['proof_status']}",
        f"theorem_problem_id: {meta['theorem_problem_id']}",
        f"determinism: {meta['determinism']}",
        f"include_triage: {meta['include_triage']}",
        f"audit_result: {result['audit_result']}",
        f"references: {result['references']}",
        f"existing_references: {result['existing_references']}",
        f"stale_references_with_candidates: {result['stale_references_with_candidates']}",
        f"missing_references_without_candidates: {result['missing_references_without_candidates']}",
        "stale_references_with_candidates:",
    ]
    stale = report["stale_references_with_candidates"]
    if not stale:
        lines.append("  - <none>")
    for ref in stale:
        lines.append(
            f"  - {ref['file']}:{ref['line']} {ref['reference']}"
        )
        for candidate in ref["candidates"]:
            lines.append(f"      candidate: {candidate}")

    missing = report["missing_references_without_candidates"]
    lines.append("missing_references_without_candidates:")
    if not missing:
        lines.append("  - <none>")
    for ref in missing:
        lines.append(
            f"  - {ref['file']}:{ref['line']} {ref['reference']}"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    parser.add_argument(
        "--include-triage",
        action="store_true",
        help="Also scan historical PR triage notes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(include_triage=args.include_triage)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
