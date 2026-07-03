# list_datasets_tutorial.py
# https://cloud.google.com/bigquery/docs/listing-datasets
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# List of all dataset objects
datasets = list(client.list_datasets())  # Make an API request.
project = client.project

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:
        print("\t{}".format(dataset.dataset_id))
else:
    print("{} project does not contain any datasets.".format(project))
