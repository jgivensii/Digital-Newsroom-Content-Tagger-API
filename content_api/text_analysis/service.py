from content_api.aws.comprehend import get_text_entities, get_text_key_phrases, dedupe_entities, dedupe_phrases
from content_api.extensions import db
from content_api.responses import ApiError
from models_api.text_analysis.db_text_analysis_model import TagExtractionRecord
from models_api.text_analysis.text_analysis_model import TagExtraction, TrendingEntityDTO
from models_api.article.article_model import Article
from models_api.article.db_article_model import ArticleRecord
from models_api.publication.db_publication_model import PublicationRecord
from sqlalchemy import select, func, true, literal, text
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
import os


COMPREHEND_MIN_CONFIDENCE = float(os.environ.get("COMPREHEND_MIN_CONFIDENCE", 75))


def create_key_phrase_tags(article_id:uuid4):
  try: 
    tag_id = uuid4()
    stmt = select(ArticleRecord.body).where(ArticleRecord.id == article_id)
    article_body = db.session.execute(stmt).scalar_one()

    #Defines Key Phrases
    key_phrases = get_text_key_phrases(Text_Input=article_body, Native_language='en')
    #Deduplicates key phrases
    key_phrases = dedupe_phrases(key_phrases)
    #Filters by Confidence threshold    
    key_phrases = [
        kp for kp in key_phrases
        if kp["Confidence"] * 100 >= COMPREHEND_MIN_CONFIDENCE
    ]
    
    #Defines entities
    entities = get_text_entities(Text_Input=article_body, Native_Language='en')
    #Depuplicates entities
    entities = dedupe_entities(entities)            
    #Filters by Confidence threshold
    entities = [
        ent for ent in entities
        if ent["Confidence"] * 100 >= COMPREHEND_MIN_CONFIDENCE
    ]

    tag_record = TagExtractionRecord(
        id=tag_id,
        article_id=article_id,
        body = article_body,
        tags = key_phrases,
        entities = entities
    )
    db.session.add(tag_record)
    db.session.commit()
  except Exception as e:
    print("TAG EXTRACTION ERROR (inner):", e)
    raise ApiError(code="failed dependency", status=424)
    
  return TagExtraction.model_validate(tag_record)


def count_entitites(publication_id=None) -> list:

    entity_subq = (
        select(
            TagExtractionRecord.article_id,
            func.jsonb_array_elements(TagExtractionRecord.entities).cast(JSONB).label("ent"),
        ).subquery()
    )

    entity_text = entity_subq.c.ent["Entity_Text"].astext

    stmt = (
        select(
            PublicationRecord.id.label("publication_id"),
            entity_text.label("entity"),
            func.count().label("occurrences"),
        )
        .select_from(entity_subq)
        .join(ArticleRecord, entity_subq.c.article_id == ArticleRecord.id)
        .join(PublicationRecord, ArticleRecord.publication_id == PublicationRecord.id)
        .group_by(PublicationRecord.id, entity_text)
        .order_by(func.count().desc())
        .limit(50)
    )

    # Filter to the requested publication when provided
    if publication_id is not None:
        stmt = stmt.where(PublicationRecord.id == publication_id)

    rows = db.session.execute(stmt).mappings().all()

    clean_rows = [
        row for row in rows
        if isinstance(row["entity"], str) and row["entity"].strip() != ""
    ]

    return [TrendingEntityDTO.model_validate(row) for row in clean_rows]


def tag_search(tag_name: str, publication_id: str | None = None) -> list[Article]:
    tag_subq = (
        select(
            TagExtractionRecord.article_id,
            func.jsonb_array_elements(TagExtractionRecord.tags).cast(JSONB).label("tag")
        ).subquery()
    )

    key_phrase = tag_subq.c.tag["Key_Phrase"].astext

    stmt = (
        select(ArticleRecord)
        .join(tag_subq, tag_subq.c.article_id == ArticleRecord.id)
        .where(func.lower(key_phrase) == func.lower(tag_name))
    )

    if publication_id:
        stmt = stmt.where(ArticleRecord.publication_id == publication_id)

    rows = db.session.execute(stmt).scalars().all()

    return [Article.model_validate(row) for row in rows]