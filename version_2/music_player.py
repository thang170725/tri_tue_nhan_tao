import os
import random
import unicodedata
import pygame

# Hàm bỏ dấu tiếng Việt để tìm kiếm dễ hơn
def no_accent_vietnamese(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Khởi tạo pygame mixer
pygame.mixer.init()
SONG_DIR = "songs"

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
def play_song_by_name(keyword):
    keyword = no_accent_vietnamese(keyword).lower()
    found = [s for s in songs if keyword in no_accent_vietnamese(s.lower())]
    if found:
        song = found[0]
        pygame.mixer.music.load(os.path.join(SONG_DIR, song))
        pygame.mixer.music.play()
        print(f"🎶 Đang phát: {song}")
    else:
        print("❌ Không tìm thấy bài hát phù hợp.")

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
