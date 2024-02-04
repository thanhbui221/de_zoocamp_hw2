from mage_ai.settings.repo import get_repo_path
from google.cloud import storage
from pandas import DataFrame
from os import path
import pyarrow.parquet as pq
import pyarrow as pa

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    
    """
    
    # Create a storage client
    storage_client = storage.Client()
    bucket_name = 'green_taxi_bt1'
    object_key = 'green_taxi'

    df.set_index('lpep_pickup_date', inplace=True)

    for date_value, partition_df in df.groupby('lpep_pickup_date'):

        # Specify GCS object key with partitioned folder structure
        object_key = f'green_taxi/{date_value.strftime("%Y/%m/%d")}/data.csv'

        # Get the bucket
        bucket = storage_client.bucket(bucket_name)

        # Get a blob (object) within the bucket
        blob = bucket.blob(object_key)

        # Convert partitioned DataFrame to CSV and upload to GCS
        blob.upload_from_string(partition_df.to_csv(sep='\t', index=True))

