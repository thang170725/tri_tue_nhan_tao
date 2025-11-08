'''
=============================================
====== MQTT PUBLISHER (FLASK GỌI TỚI) =======
====== GỬI LỆNH MQTT ========================
=============================================
'''

import paho.mqtt.client as mqtt
from tri_tue_nhan_tao.backend.modules.input_sound_processor import TTS

tts = TTS()

BROKER = "localhost"
TOPIC = "iot/control"

# Danh sách trạng thái thiết bị
devices = {
    "quat": False,
    "den": False,
    "cua": False
}

def on_connect(client, userdata, flags, rc):
    print("✅ Kết nối MQTT thành công.")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📨 Nhận lệnh: {payload}")

    try:
        device, action = payload.split(":")
    except ValueError:
        print("❌ Dữ liệu không hợp lệ.")
        return

    response = ""

    if device == "quat":
        if action == "on":
            devices["quat"] = True
            response = "Đã bật quạt."
        elif action == "off":
            devices["quat"] = False
            response = "Đã tắt quạt."

    elif device == "den":
        if action == "on":
            devices["den"] = True
            response = "Đã bật đèn."
        elif action == "off":
            devices["den"] = False
            response = "Đã tắt đèn."

    elif device == "cua":
        if action == "open":
            devices["cua"] = True
            response = "Đã mở cửa."
        elif action == "close":
            devices["cua"] = False
            response = "Đã đóng cửa."

    if response:
        return response
    else:
        return "không nhận được lệnh"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🚀 Đang chờ lệnh MQTT...")
client.connect(BROKER, 1883, 60)
client.loop_forever()
