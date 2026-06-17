# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate the virtual environment (must be done first)
source ../venv/Scripts/activate        # Git Bash / POSIX
..\venv\Scripts\Activate.ps1           # PowerShell

# Run the development server
python app.py                          # starts on http://localhost:5001

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test by name
pytest -k "test_login_success"
```

The SQLite database file (`expense_tracker.db`) is git-ignored and created at runtime by `init_db()`.

## Architecture

This is a **Flask + SQLite** web app. There is no ORM — all SQL is written by hand via the `sqlite3` stdlib module.

### Request flow

`app.py` is the single entry point. Every route lives there. It calls helpers from `database/db.py` for all DB work, then passes data directly to Jinja2 templates.

### Database layer (`database/db.py`)

Three functions drive everything:

- `get_db()` — opens a SQLite connection with `row_factory = sqlite3.Row` (so rows behave like dicts) and `PRAGMA foreign_keys = ON`.
- `init_db()` — creates tables with `CREATE TABLE IF NOT EXISTS`. Call once on startup or via a CLI command.
- `seed_db()` — inserts sample rows for local development.

The DB file path is `expense_tracker.db` at the project root.

### Templating

All templates extend `templates/base.html`, which provides the navbar and footer. The Jinja2 block structure is:

- `{% block title %}` — page `<title>`
- `{% block content %}` — main page body
- `{% block scripts %}` — optional JS at the end of `<body>`

### CSS conventions

All styles live in `static/css/style.css`. Design tokens are CSS custom properties on `:root` — use them, don't hardcode colours or radii. Key tokens:

- `--ink` / `--ink-soft` / `--ink-muted` — text hierarchy
- `--paper` / `--paper-warm` / `--paper-card` — background hierarchy
- `--accent` (dark green) / `--accent-2` (amber) — brand colours
- `--font-display` (DM Serif Display) / `--font-body` (DM Sans)
- `--radius-sm` / `--radius-md` / `--radius-lg` — border radii

Content sections use a white `--paper-card` card with a `1px var(--border)` border and `var(--radius-md)` corners. Legal/static pages use the `.legal-card` variant (adds a `3px var(--accent)` top border and `h2` dividers). Auth pages use `.auth-card`.

### Placeholder routes

Several routes in `app.py` return plain strings (e.g. `"Add expense — coming in Step 7"`). These are intentional stubs for a guided student project. When implementing them, replace the string return with `render_template(...)` and add the corresponding template.
