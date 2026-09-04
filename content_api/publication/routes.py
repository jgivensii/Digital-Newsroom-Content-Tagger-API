from flask import Blueprint, jsonify, request
from content_api.publication import store
from content_api.responses import ApiError, single_publication_envelope, list_publication_envelope
from pydantic import ValidationError
from uuid import UUID

publication_bp = Blueprint("publications", __name__)


# GET /api/v1/publications
@publication_bp.get("")
def get_publications():
    
    name = request.args.get("name")
    
    if name is None:
        return list_publication_envelope(store.list_publications())
    
    return list_publication_envelope(store.list_publications(name= name))

# GET /api/v1/publications/{id}
@publication_bp.get("/<uuid:publication_id>")
def get_publication_by_id(publication_id):
    publication = store.find_publication_by_id(publication_id) 
    if publication is None:
        raise ApiError(code = "not_found", status = 400, detail = publication_id)
        
    return single_publication_envelope(publication)


@publication_bp.post("")
def create_new_publication():
    body = request.get_json(silent=True) or {}
    return single_publication_envelope(store.create_publication(body)), 201

@publication_bp.put("/<uuid:publication_id>")
def update_existing_publication(publication_id):
    body = request.get_json(silent=True) or {}
    return single_publication_envelope(store.update_publication(publication_id, body)), 200

@publication_bp.delete("/<uuid:publication_id>")
def delete_publication_by_id(publication_id):
    success = store.delete_publication(publication_id)
    if success:
        return '', 204
    return jsonify(error="not found"), 404