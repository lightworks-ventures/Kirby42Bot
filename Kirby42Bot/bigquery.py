from google.cloud import bigquery
from Kirby42Bot.config import project_id, dataset_id, table_id

# Initialize a BigQuery client
client = bigquery.Client()

# Specify your Google Cloud project ID and the ID of the dataset and table to use

# Construct a BigQuery client object.
client = bigquery.Client(project=project_id)

table_id = f"{project_id}.{dataset_id}.{table_id}"

# TODO(developer): Insert data into the table.
rows_to_insert = [
    {
        "timestamp": "2023-11-10 10:00:00", 
        "username": "user1",
        "channel": "channel1", 
        "message": "Hello, World!"
        },
    # More rows to insert...
]
errors = client.insert_rows(table_id, rows_to_insert)  # Make an API request.

assert errors == []
