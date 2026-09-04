from content_api.extensions import db
from content_api.text_analysis.service import create_key_phrase_tags
from models_api.article.article_model import Article, CreateArticleDto, UpdateArticleDto
from models_api.article.db_article_model import ArticleRecord
from models_api.text_analysis.db_text_analysis_model import TagExtractionRecord
from models_api.shared import Status, Status_analysis
from pydantic import TypeAdapter
from sqlalchemy import select, func
from uuid import uuid4, UUID
from datetime import datetime, timezone

statusAdapter = TypeAdapter(Status)
status_analysisAdapter = TypeAdapter(Status_analysis)


def list_articles(publication_id: UUID) -> list[Article]:
    stmt = select(ArticleRecord).where(ArticleRecord.publication_id == publication_id)
    rows = db.session.execute(stmt).scalars().all()
    return [Article.model_validate(row) for row in rows]

def list_articles_by_title(title: str, publication_id):
    stmt = select(ArticleRecord).where(ArticleRecord.publication_id == publication_id)
    title = title.strip()
    if title:
        stmt = stmt.where(ArticleRecord.title.ilike(f"%{title}%"))
        
    rows = db.session.execute(stmt).scalars()
    return [Article.model_validate(row) for row in rows]

def find_article_by_id(id: uuid4) -> Article | None:
    row = db.session.get(ArticleRecord, id)
    return Article.model_validate(row) if row is not None else None

def create_article(article: dict):
    valid = CreateArticleDto.model_validate(article)

    record = ArticleRecord(
        id=uuid4(),
        publication_id=valid.publication_id,   # route injects this
        author=valid.author,
        title=valid.title,
        body=valid.body,

        # REQUIRED FIELDS WITH DEFAULTS
        status="draft",
        status_analysis="pending",
        
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.session.add(record)
    db.session.flush()

    try:
        create_key_phrase_tags(article_id=record.id)
        record.status_analysis = 'complete'
    except Exception as e:
        # Tag extraction failure should not block article creation.
        # Mark it as failed and carry on — the article is still saved.
        record.status_analysis = 'failed'
        print("TAG EXTRACTION ERROR:", e)

    db.session.commit()

    return Article.model_validate(record)


def update_article(id: uuid4, article: dict) -> Article | None:
    valid_update = UpdateArticleDto.model_validate(article)
    
    record = db.session.get(ArticleRecord, id)
    
    if record is None:
        return None
    
    record.author = valid_update.author
    record.title = valid_update.title
    record.body = valid_update.body
    
    db.session.commit()
    
    return Article.model_validate(record)

def delete_article(id: uuid4):
    record = db.session.get(ArticleRecord, id)
    if record is None:
        return False
    
    db.session.delete(record)
    
    db.session.commit()
    return True