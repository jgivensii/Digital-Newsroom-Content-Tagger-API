
from content_api.aws_config import get_client

def whoami():
    client = get_client("sts")
    identity = client.get_caller_identity()
    return {
        "account":identity["Account"],
        "arn":identity["Arn"]
    }