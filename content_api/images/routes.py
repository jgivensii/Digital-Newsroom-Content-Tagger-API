from flask import Blueprint, request
from content_api.responses import single_image_envelope
from content_api.images import service

image_bp = Blueprint("analyze", __name__)

UPLOAD_FILE = "File"

@image_bp.post("/<uuid:publication_id>/articles/<uuid:article_id>/analyze")
def analyze_images(publication_id, article_id):
    return single_image_envelope(service.upload_image(publication_id, article_id))
