from flask import Flask, request
import requests
import base64

# --- CONFIGURATION TTN ---
APP_ID = "demo-stm32"
DEVICE_ID = "my-stm32-node"
WEBHOOK_ID = "auto-downlink"
TTN_API_KEY = "NNSXS.VBZCX25HRNG3PE555LYCNK4X4IFFIAIKD3XOFJA.6SSES2LP2L23YYMMMZQXMIVYOCGUV25FLIYCBO7U26QVCIOK3BVA"
# -------------------------

app = Flask(__name__)

@app.route("/uplink", methods=["POST"])
def uplink_received():
    data = request.json
    print("Uplink reçu :", data)

    try:
        payload = data["uplink_message"]["frm_payload"]
        text = base64.b64decode(payload).decode()
        print(f"Message uplink décodé : {text}")
    except Exception as e:
        print("Erreur de décodage :", e)
        return "Bad payload", 400

    if text.strip().lower() == "bonjour":
        downlink = {
            "downlinks": [{
                "frm_payload": base64.b64encode(b"salut").decode(),
                "f_port": 2,
                "priority": "NORMAL"
            }]
        }

        url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{APP_ID}/webhooks/{WEBHOOK_ID}/devices/{DEVICE_ID}/down/push"
        headers = {
            "Authorization": f"Bearer {TTN_API_KEY}",
            "Content-Type": "application/json"
        }

        resp = requests.post(url, headers=headers, json=downlink)
        print("Downlink envoyé :", resp.status_code, resp.text)

    return "OK", 200


@app.route("/", methods=["GET"])
def home():
    return "Serveur TTN Auto-Downlink en ligne ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
