FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /application

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY app ./app

EXPOSE 8080

CMD ["uv", "run", "flask", "--app", "app:create_app", "run", "--host", "0.0.0.0", "--port", "8080"]