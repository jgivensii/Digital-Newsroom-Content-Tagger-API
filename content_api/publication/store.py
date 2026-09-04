from content_api.extensions import db
from models_api.publication.publication_model import Publication, CreatePublicationDto, UpdatePublicationDto
from models_api.publication.db_publication_model import PublicationRecord

from pydantic import TypeAdapter
from sqlalchemy import select, text
from uuid import uuid4



def list_publications(name: str | None = None) -> list[Publication]:
    
    stmt = select(PublicationRecord)
    if name is not None:
        stmt= stmt.where(PublicationRecord.name == name).order_by(PublicationRecord.id)

    rows = db.session.execute(stmt).scalars()
    
    return [Publication.model_validate(row) for row in rows]
    
    
def find_publication_by_id(id: uuid4) -> Publication | None:
    row = db.session.get(PublicationRecord, id)
    return Publication.model_validate(row) if row is not None else None

def create_publication(publication: dict):
    valid_publication = CreatePublicationDto.model_validate(publication)
    
    record = PublicationRecord(**valid_publication.model_dump())
    
    db.session.add(record)
    db.session.commit()
    
    return Publication.model_validate(record)

def update_publication(id: uuid4, publication: dict) -> Publication | None:
    valid_update = UpdatePublicationDto.model_validate(publication)
    
    record = db.session.get(PublicationRecord, id)
    
    if record is None:
        return None
    
    record.name = valid_update.name
    record.description = valid_update.description
    
    db.session.commit()
    
    return Publication.model_validate(record)

def delete_publication(id: uuid4):
    record = db.session.get(PublicationRecord, id)
    if record is None:
        return False
    
    db.session.delete(record)
    
    db.session.commit()
    return True