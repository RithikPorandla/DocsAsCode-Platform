# Getting Started

Welcome to **DocsAsCode** - a docs-as-code system that automates the full
documentation lifecycle: write, validate, build, and publish.

## Prerequisites

- Python 3.10+
- Git
- Docker (optional, for local builds)

## Installation

```bash
git clone https://github.com/RithikPorandla/DocsAsCode-Platform.git
cd DocsAsCode-Platform
pip install -r requirements.txt
```

## Build Docs Locally

```bash
cd docs
make html
open _build/html/index.html
```

## Run the Documentation Policy Check

The custom validator enforces rules generic linters miss:

```bash
python tools/validate_docs.py
```

## How the Pipeline Works

1. **Write** - Docs live in `/docs` as Markdown or RST alongside the code
2. **Validate** - Every pull request runs link checking, linting, and the
   custom docs-policy validator
