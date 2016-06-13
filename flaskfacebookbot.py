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
    print(data)
    messaging_events = data["entry"][0]["messaging"][0]
    print(messaging_events)
    if "message" in messaging_events and "text" in messaging_events["message"]:
        send_message(messaging_events["sender"]["id"], messaging_events["message"]["text"].encode('unicode_escape'))
    else:
        print("Do nothing")
    return "ok"

def send_message(recipient, text):

    client = Wit(WITAI_TOKEN, actions)

    session_id = 'my-user-id-42'
    context0 = client.run_actions(session_id, text, {})
    print(context0)

    data = {
        "recipient": {"id": recipient},
        "message": {"text": WitAi_returnMessage}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    global WitAi_returnMessage
    WitAi_returnMessage = msg
    print(msg)

def merge(session_id, context, entities, msg):
    math = first_entity_value(entities, 'math_expression')
    if math:
        print(math)
        context['math'] = eval(math)

    hi = first_entity_value(entities, 'usage')
    if hi:
        print(hi)
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

