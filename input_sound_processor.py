import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
import asyncio
import edge_tts
import os
import tempfile

class Recorder:
    def __init__(self, fs=44100, duration=5):
        self.fs = fs
        self.duration = duration
    
    def record_and_playback(self, filename='input.wav', save=False):
        print("bắt đầu ghi âm ...")
        audio = sd.rec(int(self.fs*self.duration), samplerate=self.fs, channels=1)
        sd.wait()
        audio_int16 = np.int16(audio*32767)
        if save:
            write(filename, self.fs, audio_int16)
            print("đã ghi âm xong và lưu vào: ", filename)
        sd.play(audio, self.fs)
        sd.wait()
        return audio_int16

class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def stt(self, filename=None, save=False):
        if filename is None: # nếu không truyền file âm thanh thì thu âm trực tiếp
            with sr.Microphone() as source:
                self.recognizer.pause_threshold = 1.5   # mặc định 0.8 giây, tăng lên thì bớt ngắt
                print("Nói gì đi...")
                audio = self.recognizer.listen(source, phrase_time_limit=15)
            if save:
                with open("temp_input.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                filename = "temp_input.wav"

        else:
            with sr.AudioFile(filename) as source:
                audio = self.recognizer.record(source)

        try:
            text = self.recognizer.recognize_google(audio, language='vi-VN')
        except sr.UnknownValueError:
            text = "không hiểu bạn nói gì"
        except sr.RequestError as e:
            print(f"lỗi kết nối: {e}")
            text = "lỗi kết nối"

        return text
    
class TTS():
    def __init__(self):
        pass
    
    def speak_vi(self, text, voice_style='northern', save=False):
        voices = {
            'northern': 'vi-VN-HoaiMyNeural',
            'southern': 'vi-VN-NamMinhNeural',
            'central': 'vi-VN-HoaiMyNeural'  # Microsoft không có voice central riêng
        }

        async def speak():
            voice_id = voices.get(voice_style, voices['northern'])
            out_file = "temp_voice.mp3" if save else os.path.join(tempfile.gettempdir(), "voice.mp3")
            communicate = edge_tts.Communicate(text=text, voice=voice_id)
            await communicate.save(out_file)
            os.system(f"mpg123 {out_file}") # nếu dùng Linux
        
        asyncio.run(speak())
        
        # os.system("start temp_voice.mp3") - nếu dùng windows

    
if __name__ == "__main__":
    # '''
    # ghi âm và nghe lại
    # '''
    # recorder = Recorder()
    # recorder.record_and_playback()

    # '''
    # ghi âm và AI nhắc lại
    # '''
    stt = STT()
    tts = TTS()

    text = stt.stt(filename=None, save=False)  # nói trực tiếp, không lưu
    print("👉 Bạn nói:", text)

    tts.speak_vi(text, voice_style='northern', save=False)  # phát lại, không lưu
