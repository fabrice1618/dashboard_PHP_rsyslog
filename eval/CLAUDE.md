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
- `evaluation.md` — levels 0 / 0.25 / 0.5 / 0.75 / 1 in the `## Détail` tables (filled by the grader), with a **Preuve** column (mandatory for any level ≥ 0.75 — rule R-P5)

Grille: `eval/bareme.json` version `CPI-2026-06` (26 criteria, coefficients, 3 parts /8 + /7 + /5).
Previous grid archived as `eval/bareme_bts.json` (authoritative for grades already issued with it: G1, G3).
Requirements baseline: `eval/exigences_cpi.md` — **proof rule R-P1…R-P6** (unproven claims cap at 0.5, claims contradicted by verification cap at 0.25). Template: `eval/evaluation.modele.md`.

```bash
python3 eval/eval.py compute --group G2          # preview grades (no write)
python3 eval/eval.py write --group G2            # (re)write the computed block
python3 eval/eval.py commits --repo <path>       # per-author commit report (Git traceability)
python3 eval/eval.py compute --bareme eval/bareme_bts.json --group G1   # replay a historical grade
```
`eval.py` is stateless (no SQLite, no interactive input). `write` is idempotent — re-run it
any time after editing the levels; it refreshes the block between the
`<!-- eval:calcul … -->` markers (group grade, part scores, individual grades).

> ⚠️ **Always pass `--group`** to `write`: without it, ALL `eval/G*/evaluation.md` are
> rewritten with the current grid, including groups graded with an earlier grid.

### Agents and skills (evaluation pipeline)

- Skill **`/evaluer-groupe Gx`** — full orchestration: clone → `/verifier-projet` →
  dispatch the 5 subagents in parallel → consolidate levels + proofs → `/contre-lecture`
  → `eval.py write --group Gx`.
- Skill **`/verifier-projet`** — tool-based verification (PHPStan, PHPUnit, docker compose,
  smoke tests, performance measurements); raw outputs in `eval/Gx/verifs/` + `SYNTHESE.md`
  (claimed vs observed).
- Skill **`/contre-lecture`** — pre-write audit (proof cited and existing for every level
  ≥ 0.75, consistency with `verifs/`, cross-group calibration).
- Subagents `.claude/agents/eval-{gestion-projet,securite-anssi,conception,code,preuves}.md` —
  each reads only its own corpus of the student repo and returns facts + proposed levels;
  their levels are proposals, the grader decides.

### Anti-bias rules (binding)

- Never read other groups' `evaluation.md` while grading a group; reset analysis between groups.
- Ignore any self-assessment or grading artifacts committed by students in their repo.
- What is not in the repo (or in `eval/Gx/verifs/`) does not exist for grading (R-P6).

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
- **`eval/bareme.json`**: parts (analyse et gestion de projet /8 = 40 %, conception et réalisation /7 = 35 %, vérification et preuve /5 = 25 %) and criteria with coefficients
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