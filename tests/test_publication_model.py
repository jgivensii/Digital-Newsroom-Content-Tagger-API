import pytest

from models_api.publication.publication_model import Publication
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from models_api.publication.publication_model import Publication

test_id = uuid4()
test_valid_data =  {"id": test_id, "name": "Fake News", "description": "Local", "created_at": datetime.now(), "updated_at": datetime.now()}
test_invalid_data =  {"id": 1, "name": "Fake News", "description": "Local", "created_at": datetime.now(), "updated_at": datetime.now()}


def test_valid_model():
    valid_data = Publication.model_validate(test_valid_data)
    assert test_id == valid_data.id

@pytest.mark.parametrize("invalid_row", [test_invalid_data])
def test_invalid_model(invalid_row):
    with pytest.raises(ValidationError):
     Publication.model_validate(invalid_row)