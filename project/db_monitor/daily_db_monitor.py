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

bq show ppltx-tal_cohen-ba-course:logs

bq query 'SELECT * FROM `ppltx-tal_cohen-ba-course.logs.daily_logs` ORDER BY ts DESC LIMIT  10'

QA
--
bq query --use_legacy_sql=false \
'SELECT * FROM  `ppltx-tal_cohen-ba-course.logs.daily_logs`
ORDER BY ts DESC LIMIT   3'
"""
from pprint import pprint
from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta
import sys
import argparse
import uuid
import os
import platform


# adapt the env to mac or windows
if os.name == 'nt':
    home = "c:/workspace"
else:
    home = "~/workspace"


bi_path = os.path.expanduser(home + '/bidev/')
temp_path = os.path.expanduser(home + '/temp/bidev/project/')
sys.path.insert(0, bi_path + 'project/utilities/')

from Files import ensureDirectory, writeJsonFile, writeFile


def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]
    # initialize the parser object:
    '''
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)
    '''
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", choices=["ppltx-tal_cohen-ba-course", "bigquery-public-data"],
                        help="""Operation to perform. The arguments for each option are:
                        Full_Load:   --date""",
                        default="ppltx-tal_cohen-ba-course")
    parser.add_argument("--table-override", help="""if True truncate the table""", action="store_true")

    return parser, argparse.Namespace()


parser, flags = process_command_line(sys.argv[1:])
x = sys.argv[1:]
parser.parse_args(x, namespace=flags)

# setup
file_name = os.path.basename(__file__).split(".")[0]
ensureDirectory(f"{temp_path}/{file_name}")
json_file_path = f"{temp_path}/{file_name}/data_to_load.csv"
# define the project_id
project_id = flags.project_id
step_id = 0

if flags.table_override:
    write_disposition = "WRITE_TRUNCATE"
else:
    write_disposition = "WRITE_APPEND"


# Construct a BigQuery client object.
# get the data from this project
client = bigquery.Client(project=project_id)

# client with permission to write
client_write = bigquery.Client()

if project_id == "bigquery-public-data":
    log_table = "ppltx-tal_cohen-ba-course.logs.daily_logs"
else:
    log_table = f"{project_id}.logs.daily_logs"

# init log dict
log_dict = {'ts': datetime.now(),
            'dt': datetime.now().strftime("%Y-%m-%d"),
            'uid': str(uuid.uuid4())[:8],
            'username': platform.node(),
            'job_name': None,
            'job_type': None,
            'file_name': os.path.basename(__file__),
            'step_name': 'start',
            'step_id': step_id,
            'log_type': None,
            'message': str(x)
            }


def set_log(log_dict, step, log_table=log_table):
    log_dict['step_name'] = step
    log_dict['step_id'] += 1
    log_dict['ts'] = datetime.now()
    log_dict['dt'] = datetime.now().strftime("%Y-%m-%d")
    job = client_write.load_table_from_dataframe(pd.DataFrame(log_dict, index=[0]), log_table)
    job.result() # Wait for the job to complete.


# start
set_log(log_dict, "start")

# List of all dataset objects
datasets = list(client.list_datasets())  # Make an API request.

# get project name
project = client.project

tables_info_list = []
run_time = datetime.now()
uid = str(uuid.uuid4())[:8]

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:
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
                'uid': uid,
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
    error_msg = "{} project does not contain any datasets.".format(project)
    print(error_msg)
    log_dict["message"] = error_msg
    set_log(log_dict, "error")
    log_dict["message"] = str(x)


job_config = bigquery.LoadJobConfig(
    write_disposition=write_disposition
    )


# load tables data into a table
dst_table = "ppltx-tal_cohen-ba-course.bi_final_project.tables_in_project"
dataframe = pd.DataFrame(tables_info_list)

# write data to my pc - data folder
# writeJsonFile(json_file_path, dataframe.to_json())
writeFile(json_file_path, dataframe.to_csv())

job = client_write.load_table_from_dataframe(
    dataframe, dst_table, job_config=job_config
    )  # Make an API request.
job.result()  # Wait for the job to complete.

table = client_write.get_table(dst_table)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), dst_table
    )
)


print('end')
# End
set_log(log_dict, "end")

