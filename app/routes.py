import os

from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
   return jsonify(message="Hello from the cloud platform API")

@routes.route('/health')
def health():
   return jsonify(status="Healthy")

@routes.route('/version')
def version():
   app_version = os.getenv("APP_VERSION", "dev")
   return jsonify(version=app_version)
