import time

from flask import Flask, g, request
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from app.telemetry import create_tracer_provider


def create_app():
    app = Flask(__name__)
    app.logger.setLevel("INFO")

    provider = create_tracer_provider()

    FlaskInstrumentor().instrument_app(
        app,
        tracer_provider=provider,
    )

    from app.routes import (
        http_request_duration_seconds,
        http_requests_total,
        routes,
    )

    @app.before_request
    def start_request_timer():
        g.request_start_time = time.perf_counter()

    @app.after_request
    def record_request_metrics(response):
        if request.path == "/metrics":
            return response

        duration = time.perf_counter() - g.request_start_time

        # Record request latency in the Prometheus histogram.
        http_request_duration_seconds.labels(path=request.path).observe(duration)

        # Record request count by endpoint and HTTP status codes - for error rate calculations.
        http_requests_total.labels(
            path=request.path,
            status=str(response.status_code),
        ).inc()

        return response

    app.register_blueprint(routes)

    return app
