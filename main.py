import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv
from random import randint

from commands import Commands

load_dotenv()

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

PERSONAL_CHANNEL = "C09TRANKTB5"

@app.event("app_mention")
def handle_mention(event, say):
    user = event["user"]
    thread_ts = event.get("thread_ts") or event["ts"]
    
    rand = randint(0, 2)
    
    match rand:
        case 0:
            say(
                text=f"<@{user}> tf is ur problem",
                thread_ts=thread_ts
            )
        case 1:
            say(
                text=f"I AM SLEEPING. DO NOT BOTHER ME",
                thread_ts=thread_ts
            )
        case 2:
            say(
                text=f":mad_ping_sock: :very-mad:",
                thread_ts=thread_ts
            )

@app.event("member_joined_channel")
def handle_join_channel(event, say):
    channel_id = event.get("channel", "")
    user_id = event.get("user", "")
    
    if channel_id != PERSONAL_CHANNEL:
        return
        
    say(
        text=f"<@{user}> welcome to my ~shithole~ channel. <@U092839T3A7> get ur ass over here."
    )

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slackbot/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask.route("/commands/test", methods=["POST"])
def cmd_test():
    data = request.form
    return Commands.test(data)

@flask.route("/commands/reminder", methods=["POST"])
def cmd_reminder():
    data = request.form
    
    return Commands.reminder(data, app)
    
if __name__ == "__main__":
    flask.run(host="0.0.0.0", port=3001)
