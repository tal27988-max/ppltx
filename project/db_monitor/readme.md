
# 📊 BigQuery Database Monitor
## Final project 


---

# 🚀 Execution

> **Note**
>
> Replace `my-project-ppltx-sql` with **your own Google Cloud Project ID** before running the script.


### Monitor your own BigQuery project

```bash
python ./project/db_monitor/daily_db_monitor_update_04.py my-project-ppltx-sql
```

### Monitor Google's Public Datasets

```bash
python ./project/db_monitor/daily_db_monitor_update_04.py bigquery-public-data
```




---

### Background
BigQuery public project contains many datasets,

It is impossible to monitor when each table had been updated

and what is the info on each table.

As a BI developer you have been requested to develop a daily job
which will monitor this data warehouse.

The job will extract the info on all the tables,

you need to define which properties you would like to extract and where to
save it.

### Action Items:
1. Define the KPIs you want to extract
2. Develop the python script which execute this operation
3. Draw a chart flow for the whole process
4. Which features will you add to the process?

---

## Solution
1. KPIs
- Created
- Last modified
- Number of rows
- Total logical bytes



---

# 📈 Metadata Collected

| Field | Description |
|--------|-------------|
| Project ID | BigQuery project |
| Dataset ID | Dataset name |
| Table ID | Table name |
| Number of Rows | Total rows |
| Table Size | Number of logical bytes |
| Created | Table creation timestamp |
| Last Modified | Last update timestamp |
| Run Time | Execution timestamp |
| Run UID | Unique execution identifier |


---

# 📖 Sources
for the code I use

[list_datasets & table](https://cloud.google.com/bigquery/docs/listing-datasets?_gl=1*1vq5pf1*_ga*MTM4MzI5MzEzMC4xNjgyOTY5Mjg0*_ga_WH2QY8WWF5*MTcxNDEzNDg4OC4zMzUuMS4xNzE0MTM0ODkwLjAuMC4w&_ga=2.201461457.-1383293130.1682969284&_gac=1.250161012.1712762613.CjwKCAjw8diwBhAbEiwA7i_sJVC0mFm6ukT01fLnYjdpPFnVGXHLIaf5VMiq6ixoNfetlBqNOJkPEhoCug0QAvD_BwE#python)

[get table info](https://cloud.google.com/bigquery/docs/tables#get_information_about_tables)

[load df to table](https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe?_gl=1*yln1py*_ga*MTM4MzI5MzEzMC4xNjgyOTY5Mjg0*_ga_WH2QY8WWF5*MTcxNDE0NDQ0NS4zMzcuMS4xNzE0MTQ0NDgxLjAuMC4w&_ga=2.223471067.-1383293130.1682969284&_gac=1.191620568.1712762613.CjwKCAjw8diwBhAbEiwA7i_sJVC0mFm6ukT01fLnYjdpPFnVGXHLIaf5VMiq6ixoNfetlBqNOJkPEhoCug0QAvD_BwE)

---
# Process
For given project_id -

we need to extract (list) all the datasets

for each dataset - we need to list all the tables

and for each table - extract the info

save all the data into a table in our project


 create schema bi_final_project OPTIONS( description = 'Contains tables from final project')


# 🔄 Process Flow

```text
BigQuery Project
        │
        ▼
List Datasets
        │
        ▼
List Tables
        │
        ▼
Extract Table Metadata
        │
        ▼
Create Pandas DataFrame
        │
        ▼
Load into BigQuery
        │
        ▼
Write Execution Log
```

---

# 📥 Output

The script stores the collected metadata in:

```text
my-project-ppltx-sql.bi_final_project.tables_in_project
```

Each execution is also logged in:

```text
my-project-ppltx-sql.logs.daily_logs
```

---


# 📂 Project Structure

```text
# 📂 Project Structure

```text
project/
└── db_monitor/
    ├── scheduler/
    │   ├── execute_daily_db_monitor_my-project-ppltx-sql.sh
    │   └── execute_daily_db_monitor_public.sh
    │
    ├── daily_db_monitor_update_04.py 
    └── README.md
```


---

# 📚 Learning Objectives

This project demonstrates:

- BigQuery Python SDK
- Metadata extraction
- ETL development
- Logging
- Python automation
- Loading Pandas DataFrames into BigQuery
- Command-line arguments using argparse


---

# 📋 Example Queries

### View monitored tables

```sql
SELECT *
FROM `my-project-ppltx-sql.bi_final_project.tables_in_project`
ORDER BY modified DESC;
```

### View execution logs

```sql
SELECT *
FROM `my-project-ppltx-sql.logs.daily_logs`
ORDER BY ts DESC
LIMIT 10;
```

---



# ⏰ Scheduler

The project includes shell scripts that can be used to automate the execution of the monitoring job.

| Script | Description |
|---------|-------------|
| `execute_daily_db_monitor_my-project-ppltx-sql.sh` | Runs the monitor against a personal BigQuery project. |
| `execute_daily_db_monitor_public.sh` | Runs the monitor against Google's public BigQuery datasets. |

These scripts are intended to be scheduled using a task scheduler such as:

- Linux Cron
- Cloud Scheduler
- CI/CD Pipeline


---

                Scheduler (.sh)
                      │
                      ▼
     daily_db_monitor_update_04.py
                      │
                      ▼
            BigQuery Metadata API
                      │
                      ▼
        Extract Tables Metadata
                      │
                      ▼
      tables_in_project (BigQuery)
                      │
                      ▼
          daily_logs (Execution Log)