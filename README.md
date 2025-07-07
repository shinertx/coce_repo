# Cluster Outlier Catalyst Engine (COCE)

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)]
(https://github.com/OWNER/REPO/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-unlicensed-lightgrey.svg)](#license)

## Overview
COCE detects pump events in micro-cap assets using social sentiment and liquidity signals. It
allocates capital with cluster-aware risk guardrails and can route trades through a convexity
sleeve for deep out-of-the-money options exposure.

## Architecture & Core Concepts
- **Pump model**: logistic classifier trained on volume and sentiment features.
- **Consensus clusters**: Louvain partitions ensure decorrelated allocations.
- **HRP allocation**: hierarchical risk parity with turnover limits.
- **Risk guardrails**: ADV cap, drawdown tracker, historical VaR floor and correlation spike
  sentinel.
- **Meta kill-switch**: trading halted if 7‑day Sharpe < 1.2 or hit rate < 0.6.

## Directory Map
```
config/             # YAML configuration
infra/              # CI workflow and Dockerfile
sim/                # back-test scripts
src/                # main package
  agent/            # orchestrators
  options/          # convexity sleeve
  execution/        # exchange adapters
  network_analysis/ # clustering & graphs
  alpha/            # feature engineering & ML classifier
  portfolio/        # allocators
  risk_guardrails/  # risk checks
  data_ingest/      # raw data loaders
  universe/         # asset filters
  state/            # persistence helpers
  utils/            # logging & config validation
tests/              # pytest suite
```

## Environment Variables
| Name | Default | Description |
|-----|---------|-------------|
| `EXCHANGE_API_KEY` | - | CEX API key for spot trades |
| `EXCHANGE_API_SECRET` | - | CEX API secret |
| `DERIBIT_CLIENT_ID` | - | Deribit API client ID |
| `DERIBIT_CLIENT_SECRET` | - | Deribit API secret |
| `TWITTER_BEARER` | "" | Twitter API bearer token |
| `COINGECKO_API_KEY` | "" | Optional CoinGecko API key |
| `SENTRY_DSN` | - | Sentry reporting DSN |
| `SLACK_WEBHOOK_URL` | - | Slack notifications |
| `LOG_LEVEL` | "INFO" | Override logging level |

## Local Dev Setup
```bash
poetry install --with dev
cp .env.example .env  # fill keys
poetry run ruff check .
poetry run mypy src
poetry run pytest --cov=src --cov-fail-under=90
docker build .  # optional
```

## Quick-Start / Testnet Guide
### Local via Poetry
```bash
poetry install && poetry run python -m src.agent.run_agent --mode sim
```
### Docker
```bash
docker build -t coce .
docker run -e $(grep -v '^#' config/base.yaml | xargs) coce
```

## Production Checklist & Liveness
- Ensure all environment variables are populated.
- Validate configs on startup (`validate_cfg`).
- CI jobs in `infra/ci.yml` must pass before deploy.
- Monitor `logs/*.jsonl` and `data/state.json` for health.

## Commands Reference
| Command | Description |
|---------|-------------|
| `python -m src.agent.run_agent --mode sim` | Run core engine in simulation |
| `python -m src.agent.run_agent --sleeve convex` | Execute convexity sleeve |
| `poetry run pytest` | Run unit tests |
| `docker build .` | Build production image |

## Post-Deploy Actions
- Verify Sentry and Slack webhooks receive events.
- Archive `logs/*.jsonl` and `data/state.json` for audit.
- Review `logs/meta_events.jsonl` weekly for kill-switch triggers.

## Risk Warnings / Kill-Switch
### Audit Status
See `AUDIT.md` for the latest audit diary. Current version 0.3 notes coverage 92 %.
### Legal Disclaimer
> WARN
> This repository is for research. Deploying live capital without independent review may
> result in loss of funds. Use at your own risk.

## Upgrade Path & Versioning
- SemVer tags in `pyproject.toml` govern releases.
- Models retrain monthly using latest labeled pump events.

## Testing & CI Matrix
- `pytest` suite covers all modules with ≥ 90 % coverage.
- Simulation scripts in `sim/` validate new strategies offline.
- GitHub Actions (`infra/ci.yml`) runs ruff, mypy and pytest with 92 % coverage gate.

## Contributing & FAQ
Follow `AGENTS.md` for code style and pull request template. Coverage must remain ≥ 90 %.

## License
No license file present. Contact maintainers for usage terms.

✅ README draft complete
