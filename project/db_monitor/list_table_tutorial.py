# list_tables_tutorial.py
# https://cloud.google.com/bigquery/docs/samples/bigquery-list-tables?
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset that contains
#                  the tables you are listing.
dataset_id = 'your-project.your_dataset'
dataset_id = "{}.py_dataset_tutorial".format(client.project)
# bigquery-public-data.baseball
dataset_id = 'bigquery-public-data.baseball'


tables = client.list_tables(dataset_id)  # Make an API request.

print("Tables contained in '{}':".format(dataset_id))
for table in tables:
    print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))


"""
table_id = 'bigquery-public-data.baseball.games_post_wide'

table = client.get_table(table_id)  # Make an API request.
"""