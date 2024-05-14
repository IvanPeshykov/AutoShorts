from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from helpers import get_random_font

class Video:

    def __init__(self, path):
        self.video_clip = VideoFileClip(path)
    
    def add_audio(self, voice):
        self.audio_clip = CompositeAudioClip([AudioFileClip(voice)])
        
    def add_subtitles(self, subtitles):
        generator = lambda txt: TextClip(txt, font=get_random_font(), fontsize=70, method='pango')
        self.subtitles = SubtitlesClip(subtitles, generator)
    
    def save(self, path):
        final = CompositeVideoClip([self.video_clip, self.subtitles.set_position(('center', 'center'), relative=True)])
        final.audio = self.audio_clip
        final.write_videofile(path, fps=60)