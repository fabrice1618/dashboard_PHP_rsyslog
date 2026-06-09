# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a student project evaluation repository. The list of groups and their members is authoritative in `groupes.ods` (run `python3 tools/cpi_eval.py roster`). **Current promotion: G1, G2, G3.**

> ⚠️ Any per-group expectations from previous promotions must NOT be used when evaluating the current promotion (G1–G3), to avoid biasing the assessment. The authoritative roster is `groupes.ods` and is not published.

Each group develops an application focused on security, logging, and web interfaces using technologies such as PHP, Docker, NextCloud, and database integration. The assignment (énoncé) lives at https://github.com/fabrice1618/dashboard_PHP_rsyslog.

## Key Commands



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
> depuis `groupes.ods` (`python3 tools/cpi_eval.py roster`) et n'est pas publiée.

### Evaluation System Architecture

The evaluation system uses a SQLite database with the following structure:
- **evaluation**: Main evaluation metadata
- **part**: Evaluation sections with max points
- **question**: Individual questions with coefficients
- **student**: Student roster
- **note**: Grades (0, 0.25, 0.5, 0.75, 1) with optional comments

Grade calculation:
1. Weighted average per section based on question coefficients
2. Section scores summed according to max points
3. Final grade normalized to /20 and rounded to nearest 0.5

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