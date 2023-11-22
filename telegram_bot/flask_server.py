import os
from dotenv import load_dotenv

import requests
from flask import Flask, request

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)


@app.route('/webhook_omni', methods=['POST'])
def webhook_omni():
    data = request.json
    if data['type'] == 'Message':
        chat_id = data['visitor']['token']
        message = data['messages'][0]['msg']
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url=url, json=payload, headers=headers)
        return 'OK', 200
    else:
        return 'Hello', 205


if __name__ == '__main__':
    app.run(host='localhost', port='5555')

