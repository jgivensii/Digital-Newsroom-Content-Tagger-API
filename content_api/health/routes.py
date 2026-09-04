from flask import Blueprint, jsonify
from content_api.health.service import whoami
from content_api.responses import error_response
from content_api.health.store import ping, db_check

health_bp = Blueprint("health", __name__)

@health_bp.get("/aws") # empty string means this endpoint will default to the given url_prefix defined in app.py
def health_aws():
    try:
        identity = whoami()
    except Exception:
        return error_response("unhealthy", 503, "Cannot Authenticate to AWS.")
    
    return jsonify(status="ok", aws=identity)

@health_bp.get("/live")     
def health_live():
    if ping():
        return jsonify(status="ok")
    return jsonify(status="down"), 500

@health_bp.get("/ready")
def health_ready():
    try: 
        db_check()
        return jsonify(status="ok")
    except Exception:
        return error_response("unhealthy", 503, "Cannot Reach Database.")
        