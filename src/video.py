from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import moviepy.video.fx.all as vfx
from helpers import get_random_font
from constants import aspect_ratio

class Video:

    def __init__(self, path):
        self.video_clip = self.crop_video(VideoFileClip(path))
        self.initial_duration = self.video_clip.duration

    def add_audio(self, voice):
        self.audio_clip = CompositeAudioClip([AudioFileClip(voice)])
        
    def add_subtitles(self, subtitles):
        random_font = get_random_font()
        generator = lambda txt, font = random_font: TextClip(txt, font = font, fontsize=40, color='white', stroke_color='black', stroke_width=3)
        self.subtitles = SubtitlesClip(subtitles, generator)

    def crop_video(self, video):
        (w, h) = video.size
        crop_width = aspect_ratio * h
        x1, x2 = (w - crop_width)//2, (w+crop_width)//2
        y1, y2 = 0, h
        return video.crop(x1=x1 , y1 = y1, x2=x2, y2 = y2)
    
    def save(self, path):
        final = CompositeVideoClip([self.video_clip, self.subtitles.set_position(('center', 'center'), relative=True)])
        final.audio = self.audio_clip
        
        # Cut video to origignal length, because subtitles can be longer than video and extend it
        final = final.subclip(0, self.initial_duration)

        final.write_videofile(path, fps=60)
        final.close()