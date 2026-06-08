#!/usr/bin/env python3
"""
DocsAsCode - documentation policy validator.

A custom CI gate that enforces documentation rules off-the-shelf linters
(doc8, pymarkdown) don't cover. Generic by design; the standards rule is a
nod to regulated technical domains (aerospace, automotive, energy) where a
reference to an engineering standard must cite an edition/year.

Rules
-----
1. Docstring coverage  - every public class/function/method documents all of
   its parameters with a ``:param name:`` entry.
2. Executable examples - doctest snippets in the source modules actually run.
3. Standards versioning - references to engineering standards (IEC/ISO/IEEE)
   in source and docs must cite a 4-digit year or ``:YYYY`` edition.

Exit code 0 = clean, 1 = violations found.
"""

from __future__ import annotations

import argparse
import ast
import doctest
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONFIG = {
    "src_dirs": ["src"],
    "docs_dirs": ["docs"],
    "standards_patterns": [
        r"IEC\s?\d{3,5}",
        r"ISO\s?\d{3,5}",
        r"IEEE\s?\d{3,5}",
    ],
    "require_param_docs": True,
    "run_doctests": True,
    "check_standards": True,
}

YEAR_RE = re.compile(r"(?::|\b)(?:19|20)\d{2}\b")


@dataclass
class Violation:
    rule: str
    location: str
    message: str

    def __str__(self) -> str:
        return f"  [{self.rule}] {self.location}\n      {self.message}"


def load_config(repo_root: Path) -> dict:
    cfg_path = repo_root / ".docpolicy.json"
    config = dict(DEFAULT_CONFIG)
    if cfg_path.exists():
        config.update(json.loads(cfg_path.read_text(encoding="utf-8")))
    return config


def _param_names(node: ast.AST) -> list[str]:
    args = node.args
    collected = []
    for group in (args.posonlyargs, args.args, args.kwonlyargs):
        collected.extend(a.arg for a in group)
    return [name for name in collected if name not in ("self", "cls")]


def check_docstring_coverage(src_files: list[Path], repo_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for path in src_files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel = path.relative_to(repo_root)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if node.name.startswith("_"):
                continue  # private / dunder symbols are exempt
            loc = f"{rel}:{node.lineno} ({node.name})"
            doc = ast.get_docstring(node) or ""
            if not doc.strip():
                violations.append(Violation("docstring", loc, "missing docstring"))
                continue
            if isinstance(node, ast.ClassDef):
                continue
            for name in _param_names(node):
                pattern = rf":param\s+(?:[^:\s]+\s+)?{re.escape(name)}\s*:"
                if not re.search(pattern, doc):
                    violations.append(
                        Violation("docstring", loc, f"parameter '{name}' is not documented")
                    )
    return violations


def check_doctests(src_files: list[Path], repo_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for path in src_files:
        mod_name = f"_docpolicy_{path.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001
            violations.append(
                Violation("doctest", str(path.relative_to(repo_root)), f"import failed: {exc}")
            )
            continue
        result = doctest.testmod(module, verbose=False, report=False)
        if result.failed:
            violations.append(
                Violation(
                    "doctest",
                    str(path.relative_to(repo_root)),
                    f"{result.failed} doctest example(s) failed",
                )
            )
    return violations


def check_standards(files: list[Path], patterns: list[str], repo_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    compiled = [re.compile(p) for p in patterns]
    for path in files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for rx in compiled:
                for match in rx.finditer(line):
                    if not YEAR_RE.search(line):
                        rel = path.relative_to(repo_root)
                        violations.append(
                            Violation(
                                "standards",
                                f"{rel}:{lineno}",
                                f"standard '{match.group(0)}' has no edition/year (e.g. ':2019')",
                            )
                        )
    return violations


def gather(dirs: list[str], suffixes: tuple[str, ...], repo_root: Path) -> list[Path]:
    found: list[Path] = []
    for d in dirs:
        base = repo_root / d
        if not base.exists():
            continue
        for suffix in suffixes:
            found.extend(p for p in base.rglob(f"*{suffix}") if "_build" not in p.parts)
    return sorted(set(found))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DocsAsCode documentation policy validator")
    parser.add_argument(
        "--root", default=".", help="Repository root (default: current directory)"
    )
    args = parser.parse_args(argv)
    repo_root = Path(args.root).resolve()
    config = load_config(repo_root)

    src_files = gather(config["src_dirs"], (".py",), repo_root)
    doc_files = gather(config["docs_dirs"], (".md", ".rst"), repo_root)

    violations: list[Violation] = []
    if config.get("require_param_docs", True):
        violations += check_docstring_coverage(src_files, repo_root)
    if config.get("run_doctests", True):
        violations += check_doctests(src_files, repo_root)
    if config.get("check_standards", True):
        violations += check_standards(
            src_files + doc_files, config["standards_patterns"], repo_root
        )

    print("DocsAsCode policy validator")
    print(f"  scanned {len(src_files)} source file(s), {len(doc_files)} doc file(s)")

    if violations:
        print(f"\nFAILED - {len(violations)} violation(s):\n")
        for v in violations:
            print(v)
        return 1

    print("\nPASSED - all documentation policy checks clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
