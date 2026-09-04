from content_api.aws_config import get_client
from content_api.config import BUCKET_NAME
from content_api.extensions import db
from content_api.aws.rekognition import get_image_labels
from models_api.images.db_image_model import ImageRecord
from models_api.article.db_article_model import ArticleRecord
from models_api.images.image_model import Images
from flask import request
from uuid import uuid4
from content_api.uploads import read_upload
from datetime import datetime, timezone
from sqlalchemy import select
import os


MAX_IMAGE_BYTES =5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
REKOGNITION_MIN_CONFIDENCE = float(os.environ.get("REKOGNITION_MIN_CONFIDENCE", 85))


def upload_image(publication_id: int, article_id: int, max_labels: int = 10) -> dict:
    image_id = uuid4()
    files = request.files.get('File') # This assumes possible user error rather than strict indexing posed by flask documentaiton request.files['file']
        
    content, filename = read_upload(file_storage=files,
                                    allowed_extension=ALLOWED_EXTENSIONS,
                                    max_bytes=MAX_IMAGE_BYTES)
    
    extension = filename.rsplit(".", 1)[-1].lower()
    object_key = f'{publication_id}/articles/{article_id}/images/{image_id}.{extension}'
    
    get_client("s3").put_object(Bucket=BUCKET_NAME, Key=object_key, Body=content)
    
    raw_labels = get_image_labels(BUCKET_NAME=BUCKET_NAME,
                              object_key=object_key,
                              max_labels=max_labels,
                              min_confidence=REKOGNITION_MIN_CONFIDENCE)
    labels = [l["name"] for l in raw_labels]
    record = db.session.query(ImageRecord).filter_by(article_id=article_id).first()

    if record:
        # update existing image
        record.featured_image_key = object_key
        record.labels = labels
        record.updated_at = datetime.now(timezone.utc)
    else:
        # create new image
        record = ImageRecord(
            id=uuid4(),
            article_id=article_id,
            featured_image_key=object_key,
            labels=labels,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(record)
    db.session.commit()
    
    return Images.model_validate(record)
    
    
    
def download_image(article_id: int):
    
    stmt = select(ImageRecord.featured_image_key).where(ImageRecord.article_id == article_id)
    object_key = db.session.execute(stmt).scalar()
    
    if object_key is not None:
        
        url = get_client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET_NAME, 
                "Key": object_key,
                "ResponseContentDisposition": "inline"},
        ExpiresIn=3600
)

        return url
    
    return None