import os

from flask import Blueprint, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

routes = Blueprint("routes", __name__)

# defining the metric
# ["endpoint"] - tracks that the counter will track separate values for different endpoints
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["endpoint"],
)

@routes.route("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

@routes.route("/")
def home():
    return jsonify(message="Hello from the cloud platform API")

# inc() increments by 1
@routes.route("/health")
def health():
    http_requests_total.labels(endpoint="/health").inc() 
    return jsonify(status="Healthy")


@routes.route("/version")
def version():
    app_version = os.getenv("APP_VERSION", "dev-v2")
    return jsonify(version=app_version)
