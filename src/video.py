from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
from helpers import get_random_item
from constants import transparent_image, video_height, video_width,  fonts, subtitles_size
from moviepy.audio.fx.volumex import volumex

class Video:

    def __init__(self, path, fileClip = ''):
        self.video_clip = fileClip if fileClip != '' else VideoFileClip(path)
        self.audio_clips = []
        self.initial_duration = self.video_clip.duration

    def add_audio(self, file, volume = 1.0):
        audio = AudioFileClip(file)
        audio = volumex(audio, volume)
        self.audio_clips.append(audio)
        
    def add_subtitles(self, subtitles):
        random_font = get_random_item(fonts)
        generator = lambda txt, font = random_font: TextClip(txt, font = font, fontsize=subtitles_size, color='white', stroke_color='black', stroke_width=3)
        self.subtitles = SubtitlesClip(subtitles, generator)

    def crop_video(self, video, percentage):
        height = video_height / 100 * percentage
        clip = crop(video, width = video_width, height = height)
        return clip.resize((video_width, height))
    
    def add_images(self, clip, percentage):
        top = self.crop_video(ImageClip(transparent_image).set_duration(clip.duration).set_position(("center","top")), percentage)
        bottom = self.crop_video(ImageClip(transparent_image).set_duration(clip.duration).set_position(("center","bottom")), percentage)
        return Video('', clips_array([[top], [clip], [bottom]]))
    
    @staticmethod
    def combine_videos(videos):
        final = concatenate_videoclips([video.video_clip for video in videos], method='compose')
        return Video('', final)
    
    def save(self, path, keep_audio = False):
        final = self.video_clip

        if hasattr(self, 'subtitles'):
            final = CompositeVideoClip([self.video_clip, self.subtitles.set_position(('center', 'center'), relative=True)])

        if keep_audio:
            self.audio_clips.append(final.audio)

        audio = CompositeAudioClip(self.audio_clips)
        final.audio = audio
        
        # Cut video to origignal length, because subtitles can be longer than video and extend it
        final = final.subclip(0, min(self.initial_duration, audio.duration))

        final.write_videofile(path, fps = 30, preset='ultrafast')

        final.close()
        self.video_clip.close()

        return path