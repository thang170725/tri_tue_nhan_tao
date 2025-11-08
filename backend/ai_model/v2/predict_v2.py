from tri_tue_nhan_tao.backend.ai_model.v2.build_model_v2 import Model    
from tri_tue_nhan_tao.backend.modules.input_sound_processor import STT, TTS
import tri_tue_nhan_tao.backend.modules.music_player as music_player
import tri_tue_nhan_tao.backend.modules.weather_api as weather_api
import os
'''
========================================================================================
====================== DỰ ĐOÁN =========================================================
========================================================================================
'''
# Chỉ khởi tạo model, không train
m = Model(df_path='tri_tue_nhan_tao/backend/ai_model/dataset1.csv')

if __name__ == '__main__':
    tts = TTS()
    stt = STT()
    while True:
        print("===== Options =====")
        print("1: Tạo lệnh bằng cách nhập chữ")
        print("2: Taọ lệnh bằng giọng nói")
        print("0: Thoát")
        
        try:           
            option = int(input("Vui lòng chọn số"))
        except ValueError:
            print('Vui lòng nhập số hợp lệ')
            continue
        if option == 0:
            break
        elif option == 1:
            user_input = input("Bạn muốn điều khiển gì? ").strip().lower()         
        elif option == 2:
            user_input = stt.stt(filename=None, save=False).strip().lower() # nói trực tiếp không lưu 
        else:
            print("lựa chọn không hợp lệ")
            continue

        if not user_input:
            print("không nhận được lệnh")
            continue

        vec_path = "tri_tue_nhan_tao/backend/ai_model/v2/vectorizer.pkl"
        intent_model_path = "tri_tue_nhan_tao/backend/ai_model/v2/intent_model.pt"
        encoder_path = "tri_tue_nhan_tao/backend/ai_model/v2/label_encoder.pkl"

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
                tts.speak_vi(response_text, voice_style='northern', save=False)
            else:
                response_text = "🎵 Đang phát nhạc"
                tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'stop_music':
            music_player.stop_song()
            response_text = "⏹️ Dừng nhạc"
        elif intent == 'weather':
            _, weather_text = weather_api.get_weather("Hà Nội")
            tts.speak_vi(weather_text, voice_style='northern', save=False)
            response_text = weather_text
        elif intent == 'open_fan':
            # control_devices.send_command("quat", "on")
            response_text = "Đang bật quạt."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'close_fan':
            # control_devices.send_command("quat", "off")
            response_text = "Đang tắt quạt."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'turn_on_lights':
            # control_devices.send_command("den", "on")
            response_text = "Đang bật đèn."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'turn_off_lights':
            # control_devices.send_command("den", "off")
            response_text = "Đang tắt đèn."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'open_door':
            # control_devices.send_command("cua", "open")
            response_text = "Đang mở cửa."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'close_door':
            # control_devices.send_command("cua", "close")
            response_text = "Đang đóng cửa."
            tts.speak_vi(response_text, voice_style='northern', save=False)
        elif intent == 'great':
            # response_text = 'xin chào bạn, tôi có thể giúp gì cho bạn'
            tts.speak_vi(response_text, voice_style='northern', save=False)
        else:
            response_text = f"❓ Không hiểu lệnh: {user_input}"
        if user_input.lower() in ['exit', 'quit']:
            break
        