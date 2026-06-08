# DocsAsCode

> A **docs-as-code platform** that treats documentation like software — version-controlled, automatically validated, and continuously deployed. Demonstrated on a regulated (offshore-wind) SDK, but the engine is domain-agnostic.

![CI](https://github.com/RithikPorandla/DocsAsCode-Platform/actions/workflows/docs-ci.yml/badge.svg)
![Deploy](https://github.com/RithikPorandla/DocsAsCode-Platform/actions/workflows/docs-deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Sphinx](https://img.shields.io/badge/docs-Sphinx-0a7d5a.svg)
![Hosted on](https://img.shields.io/badge/hosted%20on-GitHub%20Pages-222.svg)

---

## What is this?

Documentation rots because nothing enforces its quality. Links break, code examples
go stale, API parameters get added but never documented — and nobody notices until a
user hits the gap. **DocsAsCode** fixes that by putting documentation through the same
discipline as production code: it lives in Git, every change runs through an automated
quality gate, and the published site rebuilds itself on every merge.

The headline feature is a **custom documentation-policy validator** that checks the
things off-the-shelf linters can't: not just *style*, but *substance*.

---

## The pipeline at a glance

```mermaid
flowchart LR
    A["✍️ Write docs<br/>Markdown / RST<br/>alongside code"] --> B{"Pull Request"}
    B --> C["🔎 Lint<br/>doc8 · pymarkdown"]
    C --> D["🛡️ Policy Validator<br/>params · doctests · standards"]
    D --> E["🏗️ Sphinx build<br/>-W (warnings = errors)"]
    E --> F["✅ Merge to main"]
    F --> G["🚀 Auto-deploy<br/>GitHub Pages"]
    style D fill:#0a7d5a,color:#fff
    style G fill:#11242b,color:#fff
```

Nothing reaches the live site unless it lints clean, passes the policy gate, and builds
with zero warnings.

---

## The differentiator: a documentation-policy validator

Generic linters check formatting — line length, heading levels, trailing whitespace.
They cannot tell you whether your docs are *correct*. `tools/validate_docs.py` does, by
introspecting the actual source with Python's AST and executing examples for real.

```mermaid
flowchart TD
    S["📦 Source code + docs"] --> R1["Parameter coverage<br/>(AST introspection)"]
    S --> R2["Executable examples<br/>(doctest)"]
    S --> R3["Standards versioning<br/>(IEC / ISO / IEEE cite a year)"]
    R1 --> V{"All checks pass?"}
    R2 --> V
    R3 --> V
    V -- "yes" --> P["exit 0 — CI green ✅"]
    V -- "no" --> X["exit 1 — CI fails ❌<br/>with file:line + reason"]
    style X fill:#b00020,color:#fff
    style P fill:#0a7d5a,color:#fff
```

| Rule | What it enforces | Why it matters |
|------|------------------|----------------|
| **Parameter coverage** | Every public function/method documents *all* its parameters | Catches the silent drift where code gains a parameter the docs never mention |
| **Executable examples** | `doctest` snippets in the source actually run | A copy-paste example that no longer works is worse than none |
| **Standards versioning** | References to engineering standards must cite an edition/year | An uncited standard (e.g. `IEC 61400` vs `IEC 61400-1:2019`) is a compliance risk |

Rules are configurable in `.docpolicy.json`.

### What it catches

```diff
- def compliance_report(self, site_id, standard):   # ❌ params undocumented
-     """Generate a compliance summary."""
+ def compliance_report(self, site_id, standard="IEC 61400-1:2019"):
+     """Generate a compliance summary.
+
+     :param site_id: Identifier of the wind farm site.   # ✅ now documented
+     :param standard: Standard to assess against, incl. edition/year.
+     """
```

The validator even caught a bare standard reference in this repo's own compliance
guide during development — exactly the failure mode it exists to prevent.

---

## Architecture

```mermaid
flowchart LR
    subgraph Repo["📁 Git repository"]
        SRC["src/windfarm_sdk.py<br/>(docstrings = source of truth)"]
        DOCS["docs/*.md, *.rst<br/>(guides + reference)"]
    end
    SRC -->|"Sphinx autodoc"| REF["API reference<br/>(auto-generated)"]
    DOCS --> SITE
    REF --> SITE["📘 Static HTML site"]
    SITE -->|"GitHub Actions"| PAGES["🌐 GitHub Pages"]
```

The API reference is **generated from docstrings** — edit the code, and the docs page
updates on the next build. No manual sync, no drift.

---

## Tech stack

| Tool | Role |
|------|------|
| **Sphinx** | Documentation generation engine |
| **MyST Parser** | Markdown authoring inside Sphinx |
| **Read the Docs theme** | Developer-portal styling |
| **GitHub Actions** | CI (lint + validate + build) and CD (deploy) |
| **doc8 / pymarkdown** | RST / Markdown linting |
| **linkchecker** | Broken-link detection |
| **Custom validator** | Param coverage · doctests · standards versioning |

---

## Quick start

```bash
git clone https://github.com/RithikPorandla/DocsAsCode-Platform
cd DocsAsCode-Platform
pip install -r requirements.txt

python tools/validate_docs.py   # run the policy gate
cd docs && make html            # build the site
```

Then open `docs/_build/html/index.html`. Live build: **https://RithikPorandla.github.io/DocsAsCode-Platform**

---

## Repository layout

```
.
├── .github/workflows/    # CI (lint + validate + build) and CD (deploy)
├── docs/                 # Documentation source
│   ├── conf.py           # Sphinx config
│   ├── index.rst         # Docs homepage
│   ├── getting-started.md
│   ├── compliance.md     # Guide: docs-as-code for compliance
│   └── _static/          # Custom theme accents
├── src/
│   └── windfarm_sdk.py   # Example SDK, auto-documented from docstrings
├── tools/
│   └── validate_docs.py  # ⭐ Custom documentation-policy validator
├── .docpolicy.json       # Validator configuration
└── requirements.txt
```

---

## How the pipeline works

1. **Write** — Docs live in `/docs` as Markdown or RST, version-controlled beside the code.
2. **Validate** — Every pull request runs linting, link checking, and the custom policy gate.
3. **Build** — Sphinx compiles the docs and auto-generates the API reference (`-W`: a single warning fails the build).
4. **Deploy** — A merge to `main` rebuilds and publishes to GitHub Pages automatically.

---

## Setup notes

One-time, to enable auto-deploy: **Settings → Pages → Build and deployment → Source → GitHub Actions**.

## Honest scope

This is a developer-experience / tooling project. The wind SDK is a believable *demo
domain*, not a product claim — the validator's standards rule applies equally to
aerospace (`DO-178C`), automotive (`ISO 26262:2018`), or medical-device documentation.
The transferable idea is automated documentation *quality enforcement* in CI.
