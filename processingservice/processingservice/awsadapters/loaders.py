import pandas as pd
import boto3
import requests
from io import BytesIO
from .config import STANDARD


def load_csv_from_s3(url: str, expiry: int = 3600) -> pd.DataFrame:
    s3_client = boto3.client('s3', config=STANDARD)

    # Parse bucket name and object key from the URL
    url_components = url.split('/')
    bucket_name = url_components[2].split('.')[0]
    object_key = '/'.join(url_components[3:])

    # Generate a presigned URL
    presigned_url = s3_client.generate_presigned_url('get_object',
                                                     Params={'Bucket': bucket_name, 'Key': object_key},
                                                     ExpiresIn=expiry)

    # Use the presigned URL to read the CSV file into a DataFrame
    response = requests.get(presigned_url)
    return pd.read_csv(BytesIO(response.content))
