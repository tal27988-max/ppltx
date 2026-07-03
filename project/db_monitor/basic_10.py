#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains free text

This script run queries by the configuration file
this can be used as a daily job for ETL
We added an argument for etl name

This script support variosity ETLs (Jobs)

- Init for the destination (aggregated) table
- Daily Job - delete data for specified date and add new data
- Delete data for specific date

Adding:
- Script log V
- Query monitoring
- Data validation

reference
https://github.com/googleapis/python-bigquery/blob/HEAD/samples/snippets/client_query.py

Execution commands:
--------------------
python3 ./tech/py_projects/py_basic_10/basic_10.py  ppltx-tal_cohen-ba-course --etl-name top_terms
python3 ./tech/py_projects/py_basic_10/basic_10.py  ppltx-tal_cohen-ba-course --etl-action init --etl-name int_top_terms
python3 ./tech/py_projects/py_basic_10/basic_10.py  ppltx-tal_cohen-ba-course --etl-action daily --etl-name int_top_terms
python3 ./tech/py_projects/py_basic_10/basic_10.py  ppltx-tal_cohen-ba-course --etl-action daily --etl-name int_top_terms --dry-run

"""

import os
import json
import shutil
import sys
import argparse
from google.cloud import bigquery
from datetime import datetime, timedelta
import uuid
import platform
import pandas as pd

# adapt the env to mac or windows
if os.name == 'nt':
    home = "c:/workspace"
else:
    home = "~/workspace"


# define paths
bi_path = os.path.expanduser(home + '/bidev/')
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, bi_path + 'tech/py_projects/utilities/')

from Files import readJsonFile, header, readFile, writeFile


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
        # FIXME: Do we really need to include the OAuth2 options?
        # parents=[tools.argparser]
    )
    parser.add_argument("project_id", choices=["ppltx-tal_cohen-ba-course", "ll-data-training"],
                        help="""Operation to perform. The arguments for each option are:
                        Full_Load:   --date""",
                        default="ppltx-tal_cohen-ba-course")
    parser.add_argument("--etl-action", choices=["init", "daily", "delete"], help="""The action the etl job""")
    parser.add_argument("--etl-name", help="""The name of the etl job""")
    parser.add_argument("--dry-run", help="""if True don't execute the queries""", action="store_true")
    parser.add_argument("--days-back", help="""The number of days we want to go back""",
                        default=1)

    return parser, argparse.Namespace()


parser, flags = process_command_line(sys.argv[1:])
x = sys.argv[1:]
parser.parse_args(x, namespace=flags)




# define the project_id
project_id = flags.project_id
etl_name = flags.etl_name
etl_action = flags.etl_action
days_back = int(flags.days_back)
step_id = 0
env_type = 'daily'
log_table = f"{project_id}.logs.daily_logs"

# Construct a BigQuery client object.
client = bigquery.Client(project=project_id)

# init log dict
log_dict = {'ts': datetime.now(),
            'dt': datetime.now().strftime("%Y-%m-%d"),
            'uid': str(uuid.uuid4())[:8],
            'username': platform.node(),
            'job_name': f'{etl_name}',
            'job_type': f'{etl_action}',
            'file_name': os.path.basename(__file__),
            'step_name': 'start',
            'step_id': step_id,
            'log_type': env_type,
            'message': str(x)
            }


# functions
def set_log(log_dict, step, log_table=log_table):
    log_dict['step_name'] = step
    log_dict['step_id'] += 1
    log_dict['ts'] = datetime.now()
    log_dict['dt'] = datetime.now().strftime("%Y-%m-%d")
    job = client.load_table_from_dataframe(pd.DataFrame(log_dict, index=[0]), log_table)
    job.result() # Wait for the job to complete.


if not flags.dry_run:
    set_log(log_dict, "start")

# define date
run_time = datetime.now().strftime('%Y-%m-%d')
ymd = (datetime.now() + timedelta(days=-days_back)).strftime('%Y-%m-%d')


# define the configuration of the etl action file path and load / read the configuration
conf_file_name = f"{dir_path}/config/action_conf.json"
etl_conf = readJsonFile(conf_file_name)[etl_action]


# define the configuration file path and load / read the configuration
conf_file_name = f"{dir_path}/config/{etl_name}_conf.json"
query_conf = readJsonFile(conf_file_name)

for step_name in etl_conf:
    header(step_name)
    v = query_conf[step_name]

    query_file_name = f"{dir_path}/queries/{v['file_name']}.sql"
    query_var = readFile(query_file_name)
    v["date"] = ymd
    v["run_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = query_var.format(**v)
    # add log of the query
    query_log_file = f"{dir_path}/logs/{v['file_name']}.sql"
    writeFile(query_log_file, query)
    if not flags.dry_run:
        try:
            job_id = client.query_and_wait(query)  # Make an API request.
            header(f"The query id is: {job_id.job_id}")
            set_log(log_dict, step_name)

        except Exception as e:
            error_msg = e.errors[0]['message']
            print(f"We encounter an error: {error_msg}")
            #TODO Send notification to the developer

            for job in client.list_jobs(max_results=1):  # API request(s)
                jobid =job.job_id
            log_dict["message"] = f"{error_msg}. job_id: {jobid}"

            set_log(log_dict, step_name)
            log_dict["message"]=str(x)



if not flags.dry_run:
    set_log(log_dict, "end")
