FROM python:3.10-slim AS builder
WORKDIR /build
COPY pyproject.toml .
RUN pip install poetry && poetry install --no-dev

FROM python:3.10-slim
RUN useradd -ms /bin/bash coce
USER coce
WORKDIR /home/coce
COPY --from=builder /build /home/coce
COPY . /home/coce
ENTRYPOINT ["poetry","run","python","-m","src.agent.run_agent","--mode","sim","--config","config/base.yaml"]
