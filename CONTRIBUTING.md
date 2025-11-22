# Contributing Guide

Thanks for your interest in improving this FTP File Transfer demo!
This document explains how to set up your environment, coding & style guidelines, how to structure commits / pull requests, and what to check before requesting a review.

---

## 1. Project Overview

This application demonstrates two approaches to file transfer:

- **Connection-Oriented (TCP)** with acknowledgments and retry logic.
- **Connectionless (UDP)** fire-and-forget line transmission.
  Frontend is built with Flask templating + a unified `static/app.js` and modular CSS using design tokens in `static/style.css`.

---

## 2. Development Environment Setup

1. Clone the repo.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Visit: http://localhost:5000

---

## 3. Directory Structure (Key Parts)

```
app.py                      # Flask entrypoint
connection_oriented_ftp.py  # TCP server & client logic
connectionless_ftp.py       # UDP server & client logic
templates/                  # Jinja2 templates (base + pages)
static/style.css            # Themed, commented stylesheet
static/app.js               # Shared front-end logic
uploads_connection_oriented/ # Received TCP files
uploads_connectionless/      # Received UDP files
CONTRIBUTING.md              # This guide
```

---

## 4. Coding Guidelines

### Python

- Follow **PEP 8** conventions (naming, spacing, imports).
- Keep functions small and focused.
- Add docstrings for any non-trivial function or class.
- Avoid global state unless necessary (server instances are acceptable for this demo).
- Use `secure_filename` (already added) for any new file-save paths.

### Frontend (HTML/CSS/JS)

- Keep page templates lean by reusing blocks from `base.html`.
- Prefer adding new CSS sections with clear comment headers (follow existing pattern).
- Use semantic HTML (`<nav>`, `<main>`, `<footer>`, etc.) and ARIA attributes when appropriate.
- Minimize inline scripts; extend `static/app.js` instead.

### Security / Robustness

- Validate file inputs (currently accepts any file). For improvements, you can restrict to text / size checks.
- Avoid trusting user-provided filenames beyond sanitized version.
- Consider adding logging instead of `print()` for future scalability.

---

## 5. Theming

- Dark theme is default; light theme toggled by adding `theme-light` class to `<body>`.
- New theme variables should be added in `:root` and overridden in `.theme-light` (or future `.theme-*`).
- Keep names semantic: `--color-primary`, not `--blue1`.

---

## 6. Commit Message Conventions

Use the following prefixes for clarity:

- `feat:` new user-facing feature
- `fix:` bug fix
- `ui:` styling / layout changes
- `refactor:` code restructuring without feature change
- `docs:` documentation / README / contributing updates
- `chore:` maintenance (cleanup, task scripts)

Examples:

```
feat: add auto-refresh for received files
ui: improve card hover shadow intensity
fix: handle UDP server crash on malformed packet
docs: add section on theme architecture
```

---

## 7. Pull Request Checklist

Before opening a PR, ensure:

- [ ] Code runs locally (`python app.py`) without exceptions.
- [ ] No syntax errors (`python -m py_compile *.py`).
- [ ] New UI components responsive (resize browser <= 400px width).
- [ ] Theme toggle still works if CSS changes were made.
- [ ] README updated if you introduced a new user feature.
- [ ] No secrets or hardcoded local paths added.

Optional but encouraged:

- [ ] Added minimal tests (if you introduce logic-heavy Python functions).
- [ ] Added comments for non-trivial sections.

---

## 8. Suggesting Enhancements

Open an Issue / Discussion describing:

- Problem / motivation
- Proposed solution (short outline)
- Scope (files likely touched)
- Any risks (performance, complexity)

---

## 9. Style / Lint Tools (Future Roadmap)

Currently no dedicated linters configured. For future improvements consider:

- `ruff` or `flake8` for Python linting
- `black` or `autopep8` for formatting
- `stylelint` / `prettier` for CSS/JS formatting

---

## 10. Performance Tips

- Increase TCP `chunk_size` for large files (currently 100 bytes) if you need throughput.
- For UDP, implement optional sequencing / checksum if reliability matters.
- Avoid blocking calls in Flask routes; consider background task queue for heavy operations.

---

## 11. Troubleshooting

| Issue                 | Possible Cause                           | Fix                                           |
| --------------------- | ---------------------------------------- | --------------------------------------------- |
| Server won't start    | Port in use                              | Change port in code (2121/2122) or free port  |
| File not received TCP | Lost ACK after max retries               | Increase `max_retries` or timeout             |
| Garbled UDP file      | Non-text / binary file sent line-by-line | Adapt UDP to send raw bytes with size framing |
| Theme not persisting  | LocalStorage blocked                     | Check browser privacy settings                |

---

## 12. Code of Conduct (Short)

Be respectful. Provide constructive feedback. Avoid derogatory language. Focus on improving the project. Harassment is not tolerated.

---

## 13. License

Contributions are made under the MIT License. By contributing you agree your code can be distributed under MIT.

---

## 14. Quick Start (TL;DR)

```
# clone & enter
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

Make your change -> commit with prefix -> open PR.

---

Thank you for helping grow this project! 🚀
