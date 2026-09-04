import boto3
from functools import lru_cache
from content_api.config import AWS_PROFILE, AWS_REGION

@lru_cache(maxsize=1)
def get_session() -> boto3.Session:
    return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)

@lru_cache(maxsize=None)
def get_client(service_name: str):
    return get_session().client(service_name)

