#!/usr/bin/env python3
"""
Simple Flask webhook + Webhook for WhatsApp Business API
to run the Yacchu Hair Garage Needle 3 AI chatbot in WhatsApp.
Requires .env with WHATSAPP_TOKEN and NUMBER_0N (phone id).
"""

import os
import json
from flask import Flask, request, jsonify
import requests

from cli_chatbot import faq_lookup

app = Flask(__name__)

# Load from .env
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("NUMBER_0N")

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Webhook verification for WhatsApp
        return "ok", 200

    data = request.get_json()
    if not data:
        return jsonify({"status": "no data"}), 400

    # Handle incoming message
    entry = data["entry"][0]
    changes = entry["changes"][0]

    # Message structure for text
    if changes["value"]["messages"]:
        msg = changes["value"]["messages"][0]
        from_phone = msg["from"]
        text = msg["text"]["body"].lower().strip()

        # Process with our chatbot
        response = faq_lookup(text)['answer']

        # Send response back to WhatsApp
        if PHONE_ID and TOKEN:
            requests.post(
                f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages",
                headers={
                    "Authorization": f"Bearer {TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": from_phone,
                    "type": "text",
                    "text": {"body": response}
                }
            )

        return jsonify({"status": "received", "from": from_phone}), 200

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    print("WhatsApp Business API chatbot running on port 5000")
    print("Set WHATSAPP_TOKEN and NUMBER_0N in .env")
    app.run(host="0.0.0.0", port=5000)

# Usage: "pip install flask requests" then run:
# 1. Set .env: WHATSAPP_TOKEN="your_token" NUMBER_0N="your_phone_id"
# 2. python3 whatsapp_chatbot.py
# 3. webhook URL to WhatsApp Business API setup
# 4. Test with /test endpoint