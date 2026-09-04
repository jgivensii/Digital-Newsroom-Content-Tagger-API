import pytest
from uuid import uuid4
from content_api.text_analysis.service import create_key_phrase_tags
from content_api.responses import ApiError


def test_empty_key_phrases(mocker):
    mocker.patch(
        "content_api.text_analysis.service.db.session.execute",
        return_value=mocker.Mock(scalar_one=lambda: "body text")
    )

    mocker.patch(
        "content_api.text_analysis.service.get_text_key_phrases",
        return_value=[]
    )
    mocker.patch(
        "content_api.text_analysis.service.get_text_entities",
        return_value=[]
    )

    # Your service wraps any failure in ApiError
    with pytest.raises(ApiError):
        create_key_phrase_tags(uuid4())


def test_malformed_key_phrases(mocker):
    mocker.patch(
        "content_api.text_analysis.service.db.session.execute",
        return_value=mocker.Mock(scalar_one=lambda: "body text")
    )

    mocker.patch(
        "content_api.text_analysis.service.get_text_key_phrases",
        return_value=[{"WrongKey": "oops"}]
    )

    with pytest.raises(ApiError):
        create_key_phrase_tags(uuid4())


def test_db_returns_none(mocker):
    mocker.patch(
        "content_api.text_analysis.service.db.session.execute",
        return_value=mocker.Mock(scalar_one=lambda: None)
    )

    with pytest.raises(ApiError):
        create_key_phrase_tags(uuid4())


def test_db_failure(mocker):
    mocker.patch(
        "content_api.text_analysis.service.db.session.execute",
        side_effect=Exception("DB down")
    )

    with pytest.raises(ApiError):
        create_key_phrase_tags(uuid4())


def test_aws_failure(mocker):
    mocker.patch(
        "content_api.text_analysis.service.db.session.execute",
        return_value=mocker.Mock(scalar_one=lambda: "body text")
    )

    mocker.patch(
        "content_api.text_analysis.service.get_text_key_phrases",
        side_effect=Exception("AWS down")
    )

    with pytest.raises(ApiError):
        create_key_phrase_tags(uuid4())
