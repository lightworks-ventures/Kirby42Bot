import logging
import socket
import threading
import requests
from datetime import datetime
import json
from google.cloud import bigquery as bq
from config import oauth_pw

# Create a logger instance
logger = logging.getLogger(__name__)

# twitch info
nickname = "Kirby42Bot"
token = oauth_pw
channels = ["#dashy", 
            "#luxdigitalchurch",
            "#jatelive", 
            "#pastorskar", 
            "#souzylive"]

# # Initialize a BigQuery Client
client = bq.Client.from_service_account_json("key.json")

table_id = 'kirby42bot.twitch_chats.twitch_chat_log'
table = client.get_table(table_id)


def connect_to_channel(nickname, token, channel):
    server = "irc.chat.twitch.tv"
    port = 6667
    sock = socket.socket()
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    # Create a custom logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s — %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

    while True:
        resp = sock.recv(2048).decode('utf-8')
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        elif len(resp) > 0:
            logging.info(resp)
            if 'kirby42bot' in resp:
                continue
            else:
                values = resp.strip().split(' — ')
                tw_message = values[0]
                username = tw_message.split('!')[0].strip(':')
                # user_handle = tw_message.split('!')[1].split(' ')[0]
                channel = tw_message.split('!')[1].split(' ')[2]
                chat_start = tw_message.find(channel)+len(channel)+2
                message = tw_message[chat_start:]
                row_to_insert = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "channel": channel,
                    "username": username,
                    "message": message
                }

                # Insert the row into the BigQuery table
                errors = client.insert_rows(table, [row_to_insert])

                if errors == []:
                    logging.debug("New rows have been added to BigQuery.")
                else:
                    logging.error(f"Error inserting row into BigQuery: {errors}")
                    continue


for channel in channels:
    logger.debug(f'starting thread: {channel}')
    t = threading.Thread(target=connect_to_channel,
                         args=(nickname, token, channel))
    t.start()
