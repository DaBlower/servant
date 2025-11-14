import os
import time
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, jsonify, request
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

@app.event("member_left_channel")
def handle_left_channel(event, say):
    user = event["user"]
    say(
        text=f"what happened to <@{user}>"
    )

flask = Flask(__name__)
handler = SlackRequestHandler(app)

@flask.route("/slackbot/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask.route("/commands/test", methods=["POST"])
def cmd_test():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    response = {
        "response_type": "ephemeral",
        "text": f"User ID: {user_id}\nChannel ID: {channel_id}"
    }

    return jsonify(response)

@flask.route("/commands/reminder", methods=["POST"])
def cmd_reminder():
    data = request.form
    user_id = data.get('user_id')
    
    if user_id != "U092839T3A7":
        res = {
            "response_type": "ephemeral",
            "text": "pls stop trying to gaslight me into thinking i have shit to do\n\nyou dont have perms to use this cmd"
        }

        return jsonify(res)

    channel_id = data.get('channel_id')
    text = data.get('text', '')
    split = text.split()

    if len(split) < 2:
        res = {
            "response_type": "ephemeral",
            "text": "noooo u need at least two argument"
        }
        return jsonify(res)
    
    minutes = split[-1]
    reminder = text.removesuffix(minutes).strip()
    
    try:
        minutes = int(minutes)
        post_at = int(time.time()) + (minutes * 60)
        
        app.client.chat_scheduleMessage(
            channel=channel_id,
            post_at=post_at,
            text=f"<@U092839T3A7> reminder: u got shit to do: {reminder}"
        )
    except ValueError:
        res = {
            "response_type": "ephemeral",
            "text": "time needs to be a number in mins"
        }
        return jsonify(res)
    
    except Exception as e:
        res = {
            "response_type": "ephemeral",
            "text": f"error: {str(e)}"
        }
        return jsonify(res)
        
    res = {
        "response_type": "ephemeral",
        "text": f"ok, will remind '{reminder}' in {minutes} minutes"
    }
    return jsonify(res)

if __name__ == "__main__":
    flask.run(host="0.0.0.0", port=3001)