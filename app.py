"""
DesiSafar — Modern Visual India Trip & Itinerary Planner
Flask backend application (Zero-JavaScript architecture).
"""

import os
from datetime import timedelta
from flask import Flask, session

from routes.main import main_bp
from routes.destinations import destinations_bp
from routes.preferences import preferences_bp
from routes.itinerary import itinerary_bp
from routes.budget import budget_bp


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "desisafar-incredible-india-secret-key-2026-v1"),
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        SESSION_COOKIE_NAME="desisafar_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if test_config:
        app.config.update(test_config)

    # Automatically ensure permanent session lifetime
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(preferences_bp)
    app.register_blueprint(itinerary_bp)
    app.register_blueprint(budget_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
