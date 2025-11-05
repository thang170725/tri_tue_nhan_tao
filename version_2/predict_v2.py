from version_2.build_model_v2 import Model    
from input_sound_processor import STT, TTS
import version_2.music_player as music_player
import version_2.weather_api as weather_api
'''
========================================================================================
====================== DỰ ĐOÁN =========================================================
========================================================================================
'''
# Chỉ khởi tạo model, không train
m = Model("dataset1.csv")

if __name__ == '__main__':
    stt = STT()
    tts = TTS()
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

        intent = m.predict(user_input, model_path="version_2/intent_model.pt", encoder_path="version_2/label_encoder.pkl")

        if intent == 'play_music':
            nomalized = music_player.no_accent_vietnamese(user_input.lower())
            if 'bat ky' in nomalized or 'ngau nhien' in nomalized:
                music_player.play_random_song()
            # else:
            #     play_song_by_name(user_input)
        elif intent == 'stop_music':
            music_player.stop_song()
        elif intent == 'weather':
            _, weather_text = weather_api.get_weather("Hà Nội")
            print(weather_text)
            tts.speak_vi(weather_text, voice_style='northern', save=False)
        if user_input.lower() in ['exit', 'quit']:
            break
        