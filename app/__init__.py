from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app.models import task

    # Register routes
    from app.routes.page_routes import page_bp
    from app.routes.task_routes import task_bp

    app.register_blueprint(page_bp)
    app.register_blueprint(task_bp, url_prefix="/api/tasks")

    @app.get("/health")
    def health():
        return jsonify({
            "status": "healthy"
        }), 200

    return app