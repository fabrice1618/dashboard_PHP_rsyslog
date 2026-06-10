# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a student project evaluation repository. The roster of each group lives in its own `eval/G*/input.json` (students + declared participation %, filled by the students). **Current promotion: G1, G2, G3.**

> ⚠️ Any per-group expectations from previous promotions must NOT be used when evaluating the current promotion (G1–G3), to avoid biasing the assessment. The `eval/G*/` directories are not published (RGPD).

Each group develops an application focused on security, logging, and web interfaces using technologies such as PHP, Docker, NextCloud, and database integration. The assignment (énoncé) lives at https://github.com/fabrice1618/dashboard_PHP_rsyslog.

## Key Commands

### Evaluation (eval.py — file-driven, re-runnable)
Sources per group in `eval/G*/`:
- `input.json` — students + participation % (filled by students)
- `evaluation.md` — levels 0 / 0.25 / 0.5 / 0.75 / 1 in the `## Détail` tables (filled by the grader)

Grille: `eval/bareme.json` (24 criteria, coefficients, parts /18 + /2). Template: `eval/evaluation.modele.md`.

```bash
python3 eval/eval.py compute             # preview group + individual grades (no write)
python3 eval/eval.py write               # (re)write the computed block into each evaluation.md
python3 eval/eval.py commits --repo <path>  # per-author commit report (Git traceability)
```
`eval.py` is stateless (no SQLite, no interactive input). `write` is idempotent — re-run it
any time after editing the levels; it refreshes the block between the
`<!-- eval:calcul … -->` markers (group grade, part scores, individual grades).

To review a group's code, clone its repo (`depot_github` in `input.json`) **inside** its
folder: `cd eval/G1 && git clone <url>` → `eval/G1/<repo-name>/`. The clone stays local
(the whole `eval/G*/` directory is gitignored — RGPD) and is the `--repo` path for `commits`.

### PHP Projects
```bash
# For PHP projects (G13, G14, G22 webapp)
# Check if project uses PHPStan
vendor/bin/phpstan analyse # Static analysis (if configured)
```

## Architecture Patterns

### Student Project Groups

> Les descriptions détaillées par groupe de l'ancienne promotion (stacks techniques,
> adresses IP de VM, identifiants, liens GitHub) ont été retirées de ce dépôt public
> pour des raisons de confidentialité. La composition de la promotion en cours est lue
> depuis `eval/G*/input.json` et n'est pas publiée.

### Evaluation System Architecture

`eval.py` reads three files and computes — no database, no hidden state:
- **`eval/bareme.json`**: parts (principal /18 = 90 %, advanced /2 = 10 %) and criteria with coefficients
- **`eval/G*/input.json`**: students + declared participation % (individualization)
- **`eval/G*/evaluation.md`**: levels (0, 0.25, 0.5, 0.75, 1) read from the `## Détail` tables, plus the grader's comments

Grade calculation:
1. Weighted average per part based on criterion coefficients
2. Part scores summed according to max points
3. Group grade normalized to /20 and rounded to nearest 0.5
4. Individual grade = group grade × (participation ÷ equal share), capped at 20
5. `write` injects the result into each `evaluation.md` between the `<!-- eval:calcul … -->` markers

## Development Workflow

### Working with Student Projects
1. Each group directory is independent
2. Projects use different tech stacks (PHP, Docker, Python)
3. Some have hardcoded credentials for demonstration
4. Documentation varies by group (README.md, procedure docs)

### Security Considerations
- Student projects contain hardcoded passwords for demonstration
- VM credentials and database passwords are documented in README files
- Projects are educational and not production-ready

## Important Notes

- No centralized package.json or build system - each group is self-contained
- Projects represent different approaches to logging/monitoring systems
- Evaluation criteria include ANSSI recommendations, installation procedures, UML diagrams, and code architecture
- PHPStan is used where available for static analysis
- Docker is used for containerized deployments in some groups