import logging
import socket
import threading
from google.cloud import bigquery
from config import oauth_pw, project_id, dataset_id, table_id

# Create a logger instance
logger = logging.getLogger(__name__)

# twitch info
nickname = "Kirby42Bot"
token = oauth_pw
channels = ["#scump", "#luxdigitalchurch", "#jatelive"]

def connect_to_channel(nickname, token, channel):
    server = "irc.chat.twitch.tv"
    port = 6667
    sock = socket.socket()
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    # # Initialize a BigQuery Client
    client = bigquery.Client(project=project_id)

    table = f"{project_id}.{dataset_id}.{table_id}"

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

            # Parse the response into a dictionary
            if resp.find('kirby42bot'):
                continue

            values = resp.strip().split(' — ')
            timestamp = values[0]
            tw_message = values[1]
            username = tw_message.split('!')[0].strip(':')

            user_handle = tw_message.split('!')[1].split(' ')[0]
            channel = tw_message.split('!')[1].split(' ')[2]
            chat_start = tw_message.find(channel)+len(channel)+2
            message = tw_message[chat_start:]
            
            row_to_insert = {
                "timestamp": timestamp,
                "channel": channel,
                "username": username,
                "message": message
            }

            # Insert the row into the BigQuery table
            errors = client.insert_rows(table, [row_to_insert])

            # If an error occurred while inserting the row, log the error
            if errors:
                logger.error(f"Error inserting row into BigQuery: {errors}")


for channel in channels:
    logger.debug(f'starting thread: {channel}')
    t = threading.Thread(target=connect_to_channel,
                        args=(nickname, token, channel))
    t.start()
