from flask import Blueprint
from content_api.responses import list_text_envelope
from content_api.text_analysis import service

tag_bp = Blueprint("tag_extraction", __name__)


@tag_bp.get("/<uuid:publication_id>/trending-entities")
def trending_entities(publication_id):
    return list_text_envelope(service.count_entitites(publication_id=publication_id))
