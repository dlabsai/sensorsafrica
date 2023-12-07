from botocore.config import Config

STANDARD = Config(
    region_name="eu-central-1",
    retries={"max_attempts": 10, "mode": "standard"},
    tcp_keepalive=True,
)
