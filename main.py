import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

@app.event("app_mention")
def handle_mention(event, say):
    user = event["user"]
    thread_ts = event.get("thread_ts") or event["ts"]
    say(
        text=f"<@{user}> tf is ur problem",
        thread_ts=thread_ts
    )

@app.event("member_joined_channel")
def handle_join_channel(event, say):
    user = event["user"]
    say(
        text=f"<@{user}> welcome to my shithole i mean channel. <@U092839T3A7> get ur ass over here."
    )

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slackbot/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask.run(host="0.0.0.0", port=3001)