# Cluster Outlier Catalyst Engine (COCE) · v0.3

Quant strategy for micro-cap pump detection with risk-governed execution.

## Quick start

Run convexity sleeve:
python -m src.agent.run_agent --sleeve convex

## Setup

Install dependencies with Poetry and copy the environment template:

```bash
poetry install --with dev
cp .env.example .env  # fill in API keys
```

## Usage

Run the agent in simulation mode:

```bash
python -m src.agent.run_agent --mode sim --config config/base.yaml
```

Launch just the convexity sleeve:

```bash
python -m src.agent.run_agent --sleeve convex
```
