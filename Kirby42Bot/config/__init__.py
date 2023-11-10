import os
from dotenv import load_dotenv

load_dotenv()

# TWITCH
oauth_pw = os.getenv('oauth_pw')

# BIGQUERY
project_id = os.getenv('project_id')
dataset_id = os.getenv('dataset_id')
table_id = os.getenv('table_id')