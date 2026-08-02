FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /application

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY app ./app

EXPOSE 8080

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]