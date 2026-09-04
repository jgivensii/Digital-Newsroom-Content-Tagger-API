import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from models_api.images.image_model import Images


def test_valid_images_model():
    test_id = uuid4()
    data = {
        "id": test_id,
        "article_id": uuid4(),
        "featured_image_key": "pub/articles/img.jpg",
        "labels": ["Cat", "Animal"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    valid = Images.model_validate(data)
    assert valid.id == test_id


def test_invalid_uuid():
    data = {
        "id": "not-a-uuid",
        "article_id": uuid4(),
        "featured_image_key": "pub/articles/img.jpg",
        "labels": ["Cat"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        Images.model_validate(data)


def test_missing_timestamp():
    data = {
        "id": uuid4(),
        "article_id": uuid4(),
        "featured_image_key": "pub/articles/img.jpg",
        "labels": ["Cat"],
        "created_at": datetime.now(),
    }
    with pytest.raises(ValidationError):
        Images.model_validate(data)


def test_empty_labels():
    data = {
        "id": uuid4(),
        "article_id": uuid4(),
        "featured_image_key": "pub/articles/img.jpg",
        "labels": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    valid = Images.model_validate(data)
    assert valid.labels == []
