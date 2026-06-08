# Compliance Documentation

This guide shows how DocsAsCode treats compliance documentation the same way it
treats code: versioned, reviewed, and automatically validated in CI.

## The problem

In regulated technical domains, documentation drifts. A manual references a
standard that has since been revised, a required section goes missing before a
submission, or a code example silently stops working. Generic linters don't
catch any of this.

## What the validator enforces

The custom check in `tools/validate_docs.py` runs on every pull request and
enforces three rules:

1. **Parameter coverage** - every public API symbol documents all its parameters.
2. **Executable examples** - doctest snippets in the SDK actually run.
3. **Standards versioning** - any reference to an engineering standard must cite
   an edition or year.

## Standards versioning, in practice

The example SDK assesses sites against **IEC 61400-1:2019**, the design
requirements standard for wind turbines. The `:2019` edition marker is what the
validator looks for - a bare reference with no edition would fail the check,
because an uncited standard is a compliance risk.

The same rule applies to any domain: **ISO 26262:2018** for automotive functional
safety or **IEEE 829-2008** for test documentation would be held to the same bar.

## Running it locally

```bash
python tools/validate_docs.py
```

A clean run exits `0`; any violation exits `1` and fails the pipeline.
