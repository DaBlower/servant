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

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slackbot/events", methods=["POST"])
def slack_events():
    return handler.handle(request)



if __name__ == "__main__":
    flask.run(host="0.0.0.0", port=3001)
