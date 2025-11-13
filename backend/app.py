'''
========================================================================================
====================== FILE CHÍNH XỬ LÝ FLASH ==========================================
========================================================================================
'''
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
from tri_tue_nhan_tao.backend.ai_model.v2 import control_devices

# --- Đường dẫn tuyệt đối cho uploads ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

# Khởi tạo model & STT/TTS
from tri_tue_nhan_tao.backend.ai_model.v2.build_model_v2 import Model    
from tri_tue_nhan_tao.backend.modules.input_sound_processor import STT, TTS
import tri_tue_nhan_tao.backend.modules.music_player as music_player
import tri_tue_nhan_tao.backend.modules.weather_api as weather_api

m = Model(os.path.join(BASE_DIR, "ai_model/dataset1.csv"))
stt = STT()
tts = TTS()

@app.route("/upload", methods=["POST"])
def upload():
    print("Nhận request upload...")

    if "file" not in request.files:
        return jsonify({"error": "Không có file"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Tên file rỗng"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    print("✅ File đã lưu:", path)

    # Chuyển giọng nói -> chữ
    try:
        m4a_path = path
        wav_path = os.path.splitext(path)[0] + ".wav"

        # Chuyển đổi
        audio = AudioSegment.from_file(m4a_path, format="m4a")  # pydub tự nhận dạng định dạng
        audio.export(wav_path, format="wav")

        user_input = stt.stt(filename=wav_path, save=False).strip().lower()
        print(f"🗣️ Lệnh từ giọng nói: {user_input}")
    except Exception as e:
        print("❌ Lỗi STT:", e)
        return jsonify({"error": "Không nhận được giọng nói"}), 500

    vec_path = os.path.join(BASE_DIR, "ai_model/v2/vectorizer.pkl")
    intent_model_path = os.path.join(BASE_DIR, "ai_model/v2/intent_model.pt")
    encoder_path = os.path.join(BASE_DIR, "ai_model/v2/label_encoder.pkl")

    # Dự đoán intent
    intent = m.predict(
        user_input,
        model_path=intent_model_path,
        vec_path=vec_path,
        encoder_path=encoder_path
    )
    print(f"🎯 Intent dự đoán: {intent}")

    # Thực thi hành động trên laptop
    response_text = ""
    if intent == 'play_music':
        nomalized = music_player.no_accent_vietnamese(user_input)
        if 'bat ky' in nomalized or 'ngau nhien' in nomalized:
            music_player.play_random_song()
            response_text = "🎵 Phát bài hát ngẫu nhiên"
        else:
            music_player.play_song_by_name(text=user_input)
            response_text = "🎵 Đang phát nhạc"
    elif intent == 'stop_music':
        music_player.stop_song()
        response_text = "⏹️ Dừng nhạc"
    elif intent == 'weather':
        _, weather_text = weather_api.get_weather("Hà Nội")
        tts.speak_vi(weather_text, voice_style='northern', save=False)
        response_text = weather_text
    elif intent == 'open_fan':
        control_devices.send_command("quat", "on")
        response_text = "Đang bật quạt."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'close_fan':
        control_devices.send_command("quat", "off")
        response_text = "Đang tắt quạt."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'turn_on_lights':
        control_devices.send_command("den", "on")
        response_text = "Đang bật đèn."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'turn_off_lights':
        control_devices.send_command("den", "off")
        response_text = "Đang tắt đèn."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'open_door':
        control_devices.send_command("cua", "open")
        response_text = "Đang mở cửa."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'close_door':
        control_devices.send_command("cua", "close")
        response_text = "Đang đóng cửa."
        tts.speak_vi(response_text, voice_style='northern', save=False)
    elif intent == 'great':
        response_text = 'xin chào bạn, tôi có thể giúp gì cho bạn'
        tts.speak_vi(response_text, voice_style='northern', save=False)
    else:
        response_text = f"❓ Không hiểu lệnh: {user_input}"

    return jsonify({
        "intent": intent,
        "command": user_input,
        "response": response_text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
