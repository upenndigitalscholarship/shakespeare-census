# Shakespeare Census

[![CI](https://github.com/upenndigitalscholarship/shakespeare-census/actions/workflows/actions.yml/badge.svg?branch=master)](https://github.com/upenndigitalscholarship/shakespeare-census/actions/workflows/actions.yml)

A database of early editions of plays attributed to Shakespeare.

**Stack:** Python 3.12 · Django 5.2 · PostgreSQL 17 · Redis

[Visit Website](https://shakespearecensus.org/)

## Setup

Requires [Docker](https://docs.docker.com/get-docker/) and [just](https://github.com/casey/just).

```bash
just bootstrap
```

This copies `.env-dist` to `.env` (if missing) and builds all Docker containers.

## Common Commands

| Command | Description |
|---|---|
| `just up` | Start the development server at http://localhost:8000 |
| `just rebuild` | Force-remove and rebuild containers from scratch |
| `just test` | Run the pytest test suite |
| `just console` | Open a bash shell in the utility container |
| `just bootstrap` | First-time setup: copy `.env` and build containers |

Run `just` with no arguments to see all available commands.

## Services

The `compose.yml` defines four services:

- **web** — Django app, exposed on port 8000
- **utility** — same image as web, used for one-off commands (migrations, tests, shell)
- **db** — PostgreSQL 17

## License

MIT
