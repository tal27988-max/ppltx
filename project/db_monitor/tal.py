#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
-----------
The job will extract the info on all the tables in the projects datasets

Reference
---------
in the readme file

Execution
---------

python ./project/db_monitor/daily_db_monitor.py ppltx-tal_cohen-ba-course
python ./project/db_monitor/daily_db_monitor.py ppltx-tal_cohen-ba-course --table-override
python ./project/db_monitor/daily_db_monitor.py bigquery-public-data --table-override


bq show ppltx-tal_cohen-ba-course:bi_final_project.tables_in_project
bq rm  ppltx-tal_cohen-ba-course:bi_final_project.tables_in_project
bq rm -f ppltx-tal_cohen-ba-course:bi_final_project.tables_in_project
bq rm -f my-project-ppltx-tal_cohen-sql:bi_final_project.tables_in_project

my-project-ppltx-tal_cohen-sql

"""


from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta

# Construct a BigQuery client object.
client = bigquery.Client()

# List of all dataset objects
datasets = list(client.list_datasets())  # Make an API request.
# get project name
project = client.project

tables_info_list = []
run_time = datetime.now()

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets :
        print("\t{}".format(dataset.dataset_id))
        dataset_id = dataset.dataset_id
        # get tables from dataset
        tables = client.list_tables(dataset_id)  # Make an API request.

        # iterate over all tables
        for table_var in tables:
            table_id = "{}.{}.{}".format(table_var.project, table_var.dataset_id, table_var.table_id)
            # print(table_id)
            table = client.get_table(table_id)  # Make an API request.
            table_info = {

                "run_time": run_time,
                "project_id": table.project,
                "dataset_id": table.dataset_id,
                "table_id": table.table_id,
                "num_rows": table.num_rows,
                "created": table.created,
                "modified": table.modified,
                "num_bytes": table.num_bytes,
            }
            tables_info_list.append(table_info)


else:
    print("{} project does not contain any datasets.".format(project))

 # load tables data into a table
dst_tables = "my-project-ppltx-tal_cohen-sql.bi_final_project.tables_in_project"
dataframe = pd.DataFrame(tables_info_list)

job = client.load_table_from_dataframe(
    dataframe, dst_tables #, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

table = client.get_table(dst_tables)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), dst_tables
    )
)

print('end')
# draft
"""

table = client.get_table(table_id)  # Make an API request.

# View table properties
print(
    "Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id)
)
print("Table dataset_id: {}".format(table.dataset_id))
print("Table table_id: {}".format(table.table_id))
print("Table modified: {}".format(table.modified))
print("Table created: {}".format(table.created))
print("Table has {} rows".format(table.num_rows))
print("Table has {} num_bytes".format(table.num_bytes))
"""

