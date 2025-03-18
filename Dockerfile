FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app


COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-root --without dev


COPY . /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
