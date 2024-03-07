# Kirby42Bot

A bot to vacuum messages from twitch and discord for eternal significance. WIP Prototype.

## How it Works:
### twitch-irc.py
Kirby leverages the [Twitch IRC API](https://dev.twitch.tv/docs/irc/) to join the chat of livestreams that are written in the code. A bot twitch account silently joins each livestream and captures each message as it's submitted. The code then pushes each message to a [Google BigQuery](https://cloud.google.com/bigquery) table as it's received. 

### kirby_gradio.py
From there, Kirby uses [Gradio](https://www.gradio.app/) to create a simple interface to view and interact with the data that is stored in BigQuery.

### chat.log
This file can be used as a debugging tool of the twitch-irc.py file

<!-- ## Set up Your Own Configuration:
- Create a Google BigQuery instance and table 
- create your own .env file
- creat your own BigQuery key.json file 
-->

## Starting the System:
- To kick off the twitch listener, type `python3 Kirby42Bot/twitch-irc.py` into the terminal.
- To kick off the gradio interface locally, type `python3 Kirby42Bot/kirby_gradio.py` into the terminal.

## Future Opportunities:
### General:
- Make these scripts deployable so they can run on an independent server and be "always-on".
- Make it easier to choose / update which accounts/channels/etc that are being ingested.
- Improve the Gradio prototype for analyzing chats.
- Use LLMs to extract key topics and interests per livestream, and per user.
- Highlight key words / topics / issues relevant to the stream owner, i.e. when someone has asked for prayer or other key things.
- Capture a transcript of the livestream to capture the streamer's conversation as well. This would enable greater context to the live discussion and what was being discussed.

### Integrations:
- Integrate with YouTube Live to accomplish the same thing that we're doing with Twitch -- <https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list>.
- Integrate with Discord to do a similar extraction method for messages sent in discord servers. This will likely require creating a discord bot that the server admin must grant permission / access to in order to accomplish this.