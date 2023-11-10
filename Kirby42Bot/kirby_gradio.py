import logging
import gradio as gr
import datetime
import numpy as np
import pandas as pd
from google.cloud import bigquery as bq

# Create a logger instance
logger = logging.getLogger(__name__)

# Initialize a BigQuery Client
client = bq.Client.from_service_account_json("key.json")

# table_id = 'kirby42bot.twitch_chats.twitch_chat_log'
# table = client.get_table(table_id)

QUERY = ('SELECT * FROM `kirby42bot.twitch_chats.twitch_chat_log` ORDER BY timestamp DESC LIMIT')


def message_count():
    message_count = ("""\
    SELECT channel, username, COUNT(*) as message_count, 
    FROM `kirby42bot.twitch_chats.twitch_chat_log`
    GROUP BY 1, 2
    ORDER BY message_count DESC""")
    
    query_job = client.query(message_count)
    query_result = query_job.result()
    df = query_result.to_dataframe()
    # Select a subset of columns
    df = df[["channel", "username", "message_count"]]
    # Convert numeric columns to standard numpy types
    df = df.astype({"message_count": np.int64})
    return df


with gr.Blocks() as demo:
    gr.Markdown("# Stream Message Count")
    with gr.Row():
        gr.DataFrame(message_count, every=5)
        # gr.ScatterPlot(message_count, every=60*60, x="confirmed_cases",
        #                y="deaths", tooltip="county", width=500, height=500)

demo.queue().launch()  # Run the demo with queuing enabled
