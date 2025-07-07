# Cluster Outlier Catalyst Engine (COCE) · v0.3

Quant strategy for micro‑cap pump detection and risk‑controlled execution.

## Overview

COCE ingests spot data, social sentiment and liquidity metrics to flag potential
micro‑cap pumps. Signals are passed through cluster‑aware allocation and strict
risk checks before orders execute via CCXT. A convexity sleeve trades deep‑OTM
options on Deribit for extra tail exposure. Weekly performance is audited by a
kill‑switch meta controller.

## Core Concepts

- **Pump model** – ARIMA filter + logistic classifier trained on volume and
  sentiment features.
- **Consensus clusters** – rolling Louvain partitions ensure decorrelated
  allocations.
- **HRP allocation** – hierarchical risk parity with per‑cluster cap and
  turnover limiter.
- **Risk guardrails** – ADV limit, drawdown tracker, historical VaR floor and
  correlation spike sentinel.
- **Meta kill‑switch** – trades halted if 7‑day Sharpe < 1.2 or hit‑rate < 0.6.

## Directory Layout

```
config/             # YAML single source of truth
infra/              # ci.yml and Dockerfile
sim/                # back‑test scripts
src/
  agent/            # run_agent entrypoint & controllers
  options/          # convexity sleeve
  execution/        # CCXT routers, slippage
  network_analysis/ # clustering & graphs
  alpha/            # feature engineering & classifier
  portfolio/        # allocators
  risk_guardrails/  # all risk checks
  data_ingest/      # loaders and scrapers
  universe/         # asset universe filters
  state/            # persistence helpers
  utils/            # logging and config validation
tests/              # pytest suite (coverage ≥ 90 %)
```

Key files:
- `src/agent/run_agent.py` – main orchestration
- `src/agent/convex_controller.py` – convexity sleeve runner
- `src/state/persistence.py` – saves `data/state.json`
- `config/base.yaml` and `config/sleeve.yaml` – default parameters

## Environment Variables

Copy `.env.example` and fill the values:

| Variable              | Purpose                     |
|---------------------- |-----------------------------|
| `EXCHANGE_API_KEY`    | CEX API key for spot trades |
| `EXCHANGE_API_SECRET` | CEX API secret              |
| `DERIBIT_CLIENT_ID`   | Deribit API client id       |
| `DERIBIT_CLIENT_SECRET` | Deribit API secret        |
| `TWITTER_BEARER`      | Twitter API bearer token    |
| `COINGECKO_API_KEY`   | CoinGecko API key (optional) |
| `SENTRY_DSN`          | Sentry error reporting      |
| `SLACK_WEBHOOK_URL`   | Slack notifications         |
| `LOG_LEVEL`           | Override logging level      |

## Local Development

```bash
poetry install --with dev
cp .env.example .env  # fill keys
poetry run ruff check .
poetry run mypy src
poetry run pytest --cov=src --cov-fail-under=90
docker build .  # optional
```

## Quick‑start / Testnet

Run the agent in simulation:

```bash
python -m src.agent.run_agent --mode sim --config config/base.yaml
```

Run only the convexity sleeve:

```bash
python -m src.agent.run_agent --sleeve convex
```

Back‑testing helpers live under `sim/`.

## Production Checklist

- All environment variables populated and configs reviewed.
- Validate configs via `validate_cfg` (imported on startup).
- Run lint, type check, tests and Docker build as above.
- Monitor `logs/trades.jsonl` and `logs/meta_events.jsonl` for liveness.
- Check `data/state.json` for persisted equity curve.

## Commands Reference

| Command                                          | Description                 |
|--------------------------------------------------|-----------------------------|
| `python -m src.agent.run_agent --mode sim`       | Run core engine in sim mode |
| `python -m src.agent.run_agent --sleeve convex`  | Execute convexity sleeve    |
| `poetry run pytest`                              | Run unit tests              |
| `docker build .`                                 | Build production image      |

## Post‑deploy Actions

- Verify Sentry and Slack hooks receive events.
- Archive `logs/*.jsonl` and `data/state.json` for audit.
- Review `logs/meta_events.jsonl` weekly for kill‑switch events.

## Risk Warnings / Kill‑switch

- `risk.max_drawdown_pct` ≤ 18
- `risk.adv_cap_pct` ≤ 2
- `sleeve.budget_pct_nav` ≤ 0.5
- Meta controller may halt trading if performance degrades.
- Use at your own risk; no live funds recommended without further review.

## Upgrade Path

1. Edit configs as needed and bump version in `pyproject.toml`.
2. Run full validation suite and update `AUDIT.md` with changes.
3. Redeploy Docker image.

## Contributing / FAQ

Pull requests must use the template in `AGENTS.md` and keep coverage ≥ 90 %.
If tests fail, check environment variables and dependency versions.

License: not provided – contact maintainers for terms.
