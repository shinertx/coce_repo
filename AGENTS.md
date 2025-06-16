### **AGENTS.md** – Contributor & AI‑Agent Guide

*(Drop this file at repo root)*

---

## 1 Project Snapshot (v0.3)

| Layer               | Purpose                                                  | Key Files / Dirs                                                                     |
| ------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Core engine**     | Cluster‑decorrelated pump detector with risk guard‑rails | `src/agent/run_agent.py`, `src/network_analysis/*`, `src/alpha/*`, `src/portfolio/*` |
| **Execution**       | Trade routing, slippage, draw‑down tracking              | `src/execution/*`, `src/risk_guardrails/*`                                           |
| **Data ingest**     | CCXT price pulls, social sentiment, volume z‑scores      | `src/data_ingest/*`                                                                  |
| **State / logging** | Persist draw‑down curve, JSONL logs                      | `src/state/*`, `src/utils/logging_utils.py`                                          |
| **Tests**           | PyTest unit + integration (coverage gate ≥ 90 %)         | `tests/`                                                                             |
| **CI**              | Ruff lint, mypy, pytest‑cov                              | `.github/workflows` → `infra/ci.yml`                                                 |

Upcoming *Convexity Sleeve* (deep‑OTM options) will live under `src/options/` and `src/agent/convex_controller.py`.

---

## 2 Local Dev / Container Setup

```bash
# one‑time
poetry install --with dev
cp .env.example .env   # fill keys

# run tests & lint
poetry run ruff check .
poetry run mypy src
poetry run pytest --cov=src --cov-fail-under=90
```

Docker image is defined in `infra/Dockerfile` (Python 3.10‑slim + Poetry).
CI replicates: `docker build .` must succeed.

---

## 3 Coding & Style Rules

* **Black**  `line‑length = 100`, Python 3.10.
* **Ruff**    treat warnings as errors.
* **Mypy**   `strict = True` except legacy stubs.
* **Tests**  Every new public function requires unit coverage; keep overall ≥ 90 % (goal 92 %).
* **Docs**   Docstring every public class / function (`"""Summary … Args: … Returns: …"""`).
* **Secrets** Never hard‑code API keys; always read via `python‑dotenv`.

---

## 4 How to validate changes

The repo already embeds a mini‑contract for AI agents:

| Validation step | Command                                | Expected                                                             |
| --------------- | -------------------------------------- | -------------------------------------------------------------------- |
| Lint            | `poetry run ruff check .`              | No warnings                                                          |
| Static types    | `poetry run mypy src`                  | 0 errors                                                             |
| Unit tests      | `poetry run pytest -q`                 | All green                                                            |
| Coverage        | `pytest --cov=src --cov-fail-under=90` | ≥ 90 %                                                               |
| Docker          | `docker build .`                       | Image builds & `python -m src.agent.run_agent --mode sim -h` exits 0 |

Agents **must run** these before finishing a task.

---

## 5 High‑risk Invariants

* **Risk budget**

  * `risk.max_drawdown_pct` ≤ 18
  * `risk.adv_cap_pct` ≤ 2
  * `sleeve.budget_pct_nav` ≤ 0.5
* **Logs** one JSON line per event; production code must call `setup_logging()`.
* **No live trading** in tests—always monkey‑patch `ccxt` / router objects.

Any PR that relaxes these limits **must** include a rationale in `AUDIT.md` and bump version.

---

## 6 Typical Codex Tasks (examples)

| Scenario                      | Mode     | Prompt “sketch”                                                                                                                         |
| ----------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Fix bug in draw‑down calc     | **CODE** | “Modify `src/execution/trade_manager.py` so `DrawdownTracker.update` is invoked; add test ensuring curve length increases after trade.” |
| Add new module                | **CODE** | “Create `src/options/deribit_router.py` with authenticated GET/POST helpers; unit‑test with requests‑mock.”                             |
| Ask for architecture overview | **ASK**  | “Explain request flow from `run_agent.py` entry to trade execution; return Mermaid diagram.”                                            |
| Coverage slipped to 89 %      | **CODE** | “Add tests for `src/universe/filter.py` error paths; restore coverage ≥ 90 %.”                                                          |

Always include:

1. **File paths** to touch.
2. **Exact commands** Codex should run for verification.
3. **Acceptance criteria** (linters, tests, CI).

---

## 7 Folder Conventions

```
src/
  agent/            # orchestrators only
  options/          # convexity sleeve (NEW)
  execution/        # exchange adapters, slippage
  network_analysis/ # graph + clustering utils
  alpha/            # feature eng + ML classifier
  portfolio/        # allocators
  risk_guardrails/  # all hard risk checks
  data_ingest/      # raw data loaders/parsers
  universe/         # asset universe filters
  utils/, state/    # helpers & persistence
sim/                # offline / back‑test scripts
config/             # YAML Single Source of Truth
tests/              # pytest suite
infra/              # ci.yml, Dockerfile
```

---

## 8 Pull‑Request Template

````
[<scope>] <summary>

### Change type
- [ ] Bug‑fix
- [ ] Feature
- [ ] Refactor / chore

### Description
<concise bullet list>

### Validation
```bash
poetry run ruff check .
poetry run mypy src
poetry run pytest --cov=src --cov-fail-under=90
docker build .
````

### Risk

*Drawdown risk unchanged (max‑DD guard still 18 %).*

Fixes #

```

---

## 9 CI / CD

CI pipeline (`infra/ci.yml`) is the single source of truth.  
Agents should **not** edit GitHub Actions unless the task explicitly states so.

---

## 10 Contact Points

* **Risk logic** – `src/risk_guardrails` owner: `@benji`  
* **Convexity sleeve** – `src/options` owner: `@quants-ai`  
* **Dev infra** – `infra/` owner: `@devops‑svc`

---

*Keep this file up to date with every structural change so human and AI contributors have a reliable contract.*
::contentReference[oaicite:0]{index=0}
```
