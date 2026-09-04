from content_api.aws_config import get_client


def get_image_labels(BUCKET_NAME: str, object_key: str, max_labels: int, min_confidence:int | None = None) -> list[dict[str]]:
    """ Calls AWS Rekognition detect_labels to extract a list of dictionaries contating image labels"""
    response = get_client("rekognition").detect_labels(Image={"S3Object": {
                                                                  'Bucket': BUCKET_NAME,
                                                                  'Name': object_key
                                                                  }}, 
                                                       MaxLabels = max_labels, 
                                                       MinConfidence = min_confidence)
    labels = [{"name": label["Name"], "confidence": round(label["Confidence"], 3)} for label in response["Labels"]]
    
    return labels    