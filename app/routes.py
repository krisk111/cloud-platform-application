import os

from flask import Blueprint, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

routes = Blueprint("routes", __name__)

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
)


@routes.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )


@routes.route("/")
def home():
    return jsonify(message="Hello from the cloud platform API")


@routes.route("/health")
def health():
    return jsonify(status="Healthy")


@routes.route("/version")
def version():
    app_version = os.getenv("APP_VERSION", "dev-v2")
    return jsonify(version=app_version)
