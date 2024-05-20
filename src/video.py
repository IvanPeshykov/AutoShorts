from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from helpers import get_random_item
from constants import aspect_ratio, fonts
from moviepy.audio.fx.volumex import volumex

class Video:

    def __init__(self, path):
        self.video_clip = self.crop_video(VideoFileClip(path))
        self.audio_clips = []
        self.initial_duration = self.video_clip.duration

    def add_audio(self, file, volume = 1.0):
        audio = AudioFileClip(file)
        audio = volumex(audio, volume)
        self.audio_clips.append(audio)
        
    def add_subtitles(self, subtitles):
        random_font = get_random_item(fonts)
        generator = lambda txt, font = random_font: TextClip(txt, font = font, fontsize=40, color='white', stroke_color='black', stroke_width=3)
        self.subtitles = SubtitlesClip(subtitles, generator)

    def crop_video(self, video):
        (w, h) = video.size
        crop_width = round(aspect_ratio * h, -1)
        x1, x2 = (w - crop_width)//2, (w+crop_width)//2
        y1, y2 = 0, h
        return video.crop(x1=x1 , y1 = y1, x2=x2, y2 = y2)
    
    @staticmethod
    def combine_videos(videos, output_path):
        final = concatenate_videoclips([video.video_clip for video in videos], method='compose')
        final.write_videofile(output_path, fps=60)
        final.close()
        return Video(output_path)
    
    def save(self, path, keep_audio = False):
        final = self.video_clip

        if hasattr(self, 'subtitles'):
            final = CompositeVideoClip([self.video_clip, self.subtitles.set_position(('center', 'center'), relative=True)])

        if keep_audio:
            self.audio_clips.append(AudioFileClip(final.audio.filename))

        audio = CompositeAudioClip(self.audio_clips)
        final.audio = audio
        
        # Cut video to origignal length, because subtitles can be longer than video and extend it
        final = final.subclip(0, min(self.initial_duration, audio.duration))

        # Cut a little bit  at the end because of the sound bug of moviepy (i guess)
        final = final.subclip(0, final.duration - 0.05)

        final.write_videofile(path, fps=60)

        final.close()
        self.video_clip.close()

        return path