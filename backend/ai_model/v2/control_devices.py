'''
=============================================
====== MQTT PUBLISHER (FLASK GỌI TỚI) =======
====== GỬI LỆNH MQTT ========================
=============================================
'''

# control_devices.py
import paho.mqtt.publish as publish

BROKER = "localhost"   # broker chạy trên máy bạn (giả lập)
PORT = 1883
TOPIC = "iot/control"

def send_command(device, action):
    """
    Gửi lệnh điều khiển thiết bị qua MQTT
    device: 'quat', 'den', 'cua'
    action: 'on' | 'off' | 'open' | 'close'
    """
    message = f"{device}:{action}"
    publish.single(TOPIC, message, hostname=BROKER, port=PORT)
    print(f"📡 Đã gửi MQTT: {message}")
