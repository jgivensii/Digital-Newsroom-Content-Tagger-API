from fastapi import APIRouter
from uuid import UUID
from client_api.clients.flask_client import flask_client
from client_api.schemas import publication_model_client, article_model_client

router = APIRouter(prefix='/client')

# ─── Publications ─────────────────────────────────────────────────────────────

@router.get("/publications", response_model=list[publication_model_client.PublicationClient])
async def get_all_publications(name: str | None = None):
    return await flask_client.get_publications(name=name)

@router.get("/publications/{publication_id}", response_model=publication_model_client.PublicationClient)
async def get_publication_by_id(publication_id: UUID):
    return await flask_client.get_publication(publication_id)

# ─── Articles ─────────────────────────────────────────────────────────────────

# NOTE: static segments (/by-tag, /search) must be declared BEFORE the
# dynamic segment (/{article_id}) so FastAPI matches them correctly.

@router.get("/publications/{publication_id}/articles", response_model=list[article_model_client.ArticleClient])
async def get_articles(publication_id: UUID):
    return await flask_client.get_articles(publication_id)

@router.get("/publications/{publication_id}/articles/by-tag", response_model=list[article_model_client.ArticleClient])
async def get_articles_by_tag(publication_id: UUID, tag: str | None = None):
    return await flask_client.get_articles(publication_id, tag=tag)

@router.get("/publications/{publication_id}/articles/search", response_model=list[article_model_client.ArticleClient])
async def search_articles(publication_id: UUID, q: str | None = None):
    return await flask_client.get_articles(publication_id, title=q)

@router.get("/publications/{publication_id}/articles/{article_id}", response_model=article_model_client.ArticleClient)
async def get_article_by_id(publication_id: UUID, article_id: UUID):
    return await flask_client.get_article(publication_id, article_id)

# ─── Trending Entities ────────────────────────────────────────────────────────

@router.get("/publications/{publication_id}/trending-entities")
async def get_trending_entities(publication_id: UUID):
    return await flask_client.get_trending_entities(publication_id=publication_id)
