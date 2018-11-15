from mutagen.mp3 import MP3 as mp3
import pygame
import time

MP3_filename = 'glass-break2.mp3'

pygame.mixer.init()
pygame.mixer.music.load(MP3_filename) #音源を読み込み
mp3_length = mp3(MP3_filename).info.length #音源の長さ取得
pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
pygame.mixer.music.stop() #音源の長さ待ったら再生停止
