import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

SLACK_BOT_TOKEN = "slack bot token xoxb-.........."
SLACK_APP_TOKEN = "slack APP token xapp-.........."
OPENAI_API_KEY = "sugeneruotas openai API raktas"

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)


# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]

    # Let the user know that we are busy with the request

    response = client.chat_postMessage(channel=body["event"]["channel"],
#                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Generuoju atsakymą!")

    # Check ChatGPT
    openai.api_key = OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message)


    # Reply to thread
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                      # thread_ts=body["event"]["event_ts"],
                                       text=f"{completion.choices[0].message.content}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
