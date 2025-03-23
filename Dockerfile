FROM python:3.12-slim


ENV PYTHONUNBUFFERED=1


WORKDIR /app


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock* /app/


RUN poetry config virtualenvs.create false \
    && poetry install --without dev  --no-root


COPY . /app/


COPY .env /app/.env


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
