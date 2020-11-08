from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

ffmpeg_extract_subclip("shorter_music.mp3", 4, 40, targetname="background.mp3")

'''
for converting .mp3 to .wav in terminal:
    ffmpeg -i background.mp3 -ab 160k -ac 2 -ar 44100 -vn audio.wav
'''