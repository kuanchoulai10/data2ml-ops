# Stage 1: Dependency installation using uv
# https://docs.astral.sh/uv/guides/integration/docker/#available-images
# https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install build tools required for psutil
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Stage 2: Final image
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

# Set the entry point for the container
ENTRYPOINT ["python", "-m", "feast_transformer"]