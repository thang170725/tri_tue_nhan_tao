import os
import random
import unicodedata
import pygame

# Hàm bỏ dấu tiếng Việt để tìm kiếm dễ hơn
def no_accent_vietnamese(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Khởi tạo pygame mixer
pygame.mixer.init()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # /backend
SONG_DIR = os.path.join(BASE_DIR, "assets", "songs")

# Lấy danh sách tất cả bài hát
songs = [f for f in os.listdir(SONG_DIR) if f.lower().endswith(('.mp3', '.wav'))]

if not songs:
    print("❌ Không tìm thấy bài hát nào trong thư mục 'songs/'. Hãy copy nhạc vào đó trước.")

# Phát nhạc ngẫu nhiên
def play_random_song():
    if not songs:
        print("⚠️ Không có bài hát để phát.")
        return
    song = random.choice(songs)
    path = os.path.join(SONG_DIR, song)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    print(f"🎵 Đang phát: {song}")

# Phát bài cụ thể theo tên
def play_song_by_name(text):
    text = text.upper()
    if 'MỞ BÀI' in text:
        text = text.replace('MỞ BÀI', '').strip()
        song = text + ' REMIX' + '.mp3'
        path = os.path.join(SONG_DIR, song)

        if not os.path.exists(path):
            print("❌ Không tìm thấy file:", path)
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print(f"🎵 Đang phát: {song}")

        # # 🕒 Giữ chương trình sống đến khi bài hát kết thúc
        # while pygame.mixer.music.get_busy():
        #     time.sleep(1)
    else:
        print("Không tìm thấy bài phù hợp")

'''
========================================================================================
====================== DỪNG PHÁT NHẠC ==================================================
========================================================================================
'''
def stop_song():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("⏹️ Đã dừng phát nhạc.")
    else:
        print("⚠️ Không có bài hát nào đang phát.")
