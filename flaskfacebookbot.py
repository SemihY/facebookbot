import requests
from flask import Flask, request
from wit import Wit

app = Flask(__name__)


ACCESS_TOKEN = "EAACg9CP50TABAD6Sm8Jz4NVSQObLkGtXL4fPFSIQAxSDzgC5Or8tc2qb8os6pmAVFO7zdCnQZAZB8sLZAsznZCcJ1y9flk5j9rzlnpNtwdFExb3lcF74ghmcZA9sGUfwF8SPqsdZBUnbcYZCSVYlmY1CPUg2GZAlmJUlE5n67z8izwZDZD"
VERIFY_TOKEN = "my_voice_is_my_password_verify_me"
WITAI_TOKEN = "O5Q4OV75PDXMSL3FX3FEXRECEBB3SD36"

WitAi_returnMessage = ""


@app.route('/', methods=['GET'])
def handle_verification():
    print("Handle  Verification")
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    print("Incoming from %s: %s" % (sender, message))
    send_message(sender, message)

    return "ok"


def send_message(token, recipient, text):

    client = Wit(WITAI_TOKEN, actions)

    session_id = 'my-user-id-42'
    client.run_actions(session_id, text, {})

    data = {
        "recipient": {"id": recipient},
        "message": {"text": WitAi_returnMessage}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


def say(session_id, context, msg):
    global WitAi_returnMessage
    WitAi_returnMessage = msg
    print(msg)

def merge(session_id, context, entities, msg):
    return context

def error(session_id, context, e):
    print(str(e))

actions = {
    'say': say,
    'merge': merge,
    'error': error,
}


if __name__ == '__main__':
    app.run()

