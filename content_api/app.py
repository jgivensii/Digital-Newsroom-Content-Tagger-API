from flask import Flask, request, g
from flask_migrate import Migrate
from pydantic import ValidationError
from uuid import uuid4
from content_api.structLogging import configure_logging
from models_api.text_analysis.db_text_analysis_model import TagExtractionRecord
from content_api.health.routes import health_bp
from content_api.publication.routes import publication_bp
from content_api.article.routes import article_bp
from content_api.images.routes import image_bp
from content_api.extensions import db
from content_api.responses import ApiError, error_response
from content_api.text_analysis.routes import tag_bp

import time, os, structlog, traceback, sys, logging

migrate = Migrate()


def create_app():
    # Initializes the Flask app
    app = Flask(__name__)

    configure_logging()
    
    logger = structlog.get_logger("app")
    
    @app.before_request 
    def start_request():
        g.correlation_id = uuid4().hex
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        duration = time.time() - g.start_time
        logger.info(
            "request_completed",
            method=request.method,
            path=request.path,
            status=response.status_code,
            duration_ms=int(duration * 1000),
            correlation_id=g.correlation_id,
        )
        return response
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(publication_bp, url_prefix = '/api/v1/publications')
    app.register_blueprint(article_bp, url_prefix='/api/v1/publications')
    app.register_blueprint(image_bp, url_prefix='/api/v1/publications')
    app.register_blueprint(tag_bp, url_prefix='/api/v1/publications')
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]      # grabbing the url value from the .env
    db.init_app(app) 
    
    migrate.init_app(app, db)
    
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):

        first_error = error.errors()[0]
        detail_str = f"{first_error['loc']}: {first_error['msg']}"
        
        # 422 - UNPROCESSABLE_ENTITY - more specific than a 400
        return error_response("validation_failed", 422, detail_str)

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        traceback.print_exc() 
        return error_response("internal", 500, "an unexpected error ocurred")

    # can handle status codes as well, not just exceptions and errors
    @app.errorhandler(404)
    def handle_resource_not_found(error):
        """ this will handle the times where FLASK throws a 404, not when your code sets the status as 404 """

        return error_response("not_found", 404, "no route for the given path")
    
    return app
