# Ogoke Works portfolio

Static site: `index.html` plus case-study images in `ba/`. No build step.

Deploy on Vercel: import this folder (or its GitHub repo) as a new project,
Framework Preset "Other", leave Build Command and Output Directory empty.
`vercel.json` rewrites `/betalmighty` to the home page, which opens the case study.

## Local preview

    python3 tests/serve.py 8080

Serves the site on http://localhost:8080 with the same `/betalmighty` rewrite as Vercel.

## End-to-end tests

Playwright tests in `tests/` drive your installed Google Chrome (no browser download).

    python3 -m venv .venv
    .venv/bin/pip install -r requirements-dev.txt
    .venv/bin/pytest                                                    # local copy, starts the server itself
    .venv/bin/pytest --base-url https://chukwuebukasportfolio.vercel.app  # the live site

`.vercelignore` keeps `tests/` and the dev files out of the deployed site.
