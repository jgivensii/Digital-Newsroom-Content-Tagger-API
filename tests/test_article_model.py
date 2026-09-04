import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from models_api.article.article_model import (
    Article,
    CreateArticleDto,
    UpdateArticleDto
)


def test_valid_article_model():
    test_id = uuid4()
    data = {
        "id": test_id,
        "publication_id": uuid4(),
        "title": "Valid Title",
        "body": "Valid body text",
        "author": "AuthorName",
        "status": "draft",
        "status_analysis": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    valid = Article.model_validate(data)
    assert valid.id == test_id


def test_invalid_uuid():
    data = {
        "id": "not-a-uuid",
        "publication_id": uuid4(),
        "title": "Valid Title",
        "body": "Valid body text",
        "author": "AuthorName",
        "status": "draft",
        "status_analysis": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        Article.model_validate(data)


@pytest.mark.parametrize("bad_title", ["", "abc", "a" * 200])
def test_title_edge_cases(bad_title):
    data = {
        "id": uuid4(),
        "publication_id": uuid4(),
        "title": bad_title,
        "body": "Valid body text",
        "author": "AuthorName",
        "status": "draft",
        "status_analysis": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        Article.model_validate(data)


@pytest.mark.parametrize("bad_body", ["", "a"])
def test_body_edge_cases(bad_body):
    data = {
        "id": uuid4(),
        "publication_id": uuid4(),
        "title": "Valid Title",
        "body": bad_body,
        "author": "AuthorName",
        "status": "draft",
        "status_analysis": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        Article.model_validate(data)


def test_create_article_dto_extra_fields():
    with pytest.raises(ValidationError):
        CreateArticleDto.model_validate({
            "title": "Valid Title",
            "publication_id": uuid4(),
            "body": "Valid body",
            "author": "AuthorName",
            "extra": "not allowed"
        })


def test_update_article_dto_missing_fields():
    with pytest.raises(ValidationError):
        UpdateArticleDto.model_validate({"title": "Valid Title"})
