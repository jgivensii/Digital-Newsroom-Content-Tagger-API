from flask import Blueprint, jsonify, request
from content_api.article import store
from content_api.images import service
from content_api.text_analysis.service import tag_search
from content_api.responses import ApiError, single_article_envelope, list_article_envelope
from pydantic import ValidationError
from uuid import UUID

article_bp = Blueprint("articles", __name__)



@article_bp.get("/<uuid:publication_id>/articles")
def get_publications(publication_id):
    tag = request.args.get("tag")
    title = request.args.get('title')
    
    if title:
        articles = store.list_articles_by_title(title=title, publication_id=publication_id)
        return list_article_envelope(articles)
    if tag:
        articles = tag_search(tag_name=tag, publication_id=publication_id)
        return list_article_envelope(articles)
    
    return list_article_envelope(store.list_articles(publication_id))
    

@article_bp.get("/<uuid:publication_id>/articles/<uuid:article_id>")
def get_ticket_by_id(publication_id, article_id):
    article = store.find_article_by_id(article_id)
    
    if article is None:
        raise ApiError(code = "not_found", status = 400, detail = article_id)
        
    article.image_url = service.download_image(article_id)
    
    return single_article_envelope(article)


# POST /api/v1/publications/<publication_id>/articles
@article_bp.post("/<uuid:publication_id>/articles")
def create_article(publication_id):
    body = request.get_json(silent=True) or {}
    body["publication_id"] = publication_id
    return single_article_envelope(store.create_article(body)), 201


@article_bp.put("/articles/<uuid:article_id>")
def update_existing_article(article_id):
    body = request.get_json(silent=True) or {}
    return single_article_envelope(store.update_article(article_id, body)), 200

@article_bp.delete("/articles/<uuid:article_id>")
def delete_article_by_id(article_id):
    success = store.delete_article(article_id)
    if success:
        return jsonify(status="deleted"), 204
    return jsonify(error="not found"), 404