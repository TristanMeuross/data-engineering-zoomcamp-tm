import io
import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc_data_lake_booming-arcana-461202-r6")



def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.parquet"

        # download it using requests via a pandas df
        request_url = f"{init_url}{file_name}"
        r = requests.get(request_url)
        save_dir = "nyc-taxi-data"
        os.makedirs(save_dir, exist_ok=True)
        local_path = os.path.join(save_dir, file_name)
        open(local_path, 'wb').write(r.content)
        print(f"Local: {local_path}")

        # upload it to gcs
        upload_to_gcs(BUCKET, f"{service}/{file_name}", local_path)
        print(f"GCS: {service}/{file_name}")

services = [
    # 'green',
    # 'fhv',
    'yellow',
]
years = ['2019', '2020']

for service in services:
    for year in years:
        web_to_gcs(year, service)


