from moviepy.editor import *

class Video:

    def __init__(self, path):
        self.video_clip = VideoFileClip(path)
    
    def add_audio(self, voice):
        self.audio_clip = CompositeAudioClip([AudioFileClip(voice)])
    
    def save(self, path):
        final = CompositeVideoClip([self.video_clip])
        final.audio = self.audio_clip
        final.write_videofile(path)