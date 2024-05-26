import numpy, cv2
from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
from helpers import get_random_item, is_image, is_video
from PIL import Image
from constants import transparent_image, video_height, video_width,  fonts, subtitles_size, max_video_length
from moviepy.audio.fx.volumex import volumex

class Video:

    def __init__(self, path, fileClip = ''):

        if fileClip != '':
            self.video_clip = fileClip
        
        elif is_video(path):
            self.video_clip = VideoFileClip(path)

        elif is_image(path):
            self.video_clip = Video.image_to_video(path)

        else:
            raise ValueError("Please provide correct path!")  

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
    
    @staticmethod 
    def image_to_video(path):

        clip_img = (
        ImageClip(path)
        .set_position(('center', 'center'))
        .set_duration(max_video_length)
        .set_fps(30)
        )

        clip_img = zoom_in_effect(clip_img, 0.04)

        clip = CompositeVideoClip([clip_img])
        return clip
    
    def save(self, path, keep_audio = False):
        final = self.video_clip

        if hasattr(self, 'subtitles'):
            final = CompositeVideoClip([self.video_clip, self.subtitles.set_position(('center', 'center'), relative=True)])

        if keep_audio:
            self.audio_clips.append(final.audio)

        audio = CompositeAudioClip(self.audio_clips)
        final.audio = audio
        
        # Cut video to origignal length, because subtitles can be longer than video and extend it
        final = final.subclip(0,min(self.initial_duration, audio.duration, max_video_length))

        final.write_videofile(path, fps = 30, preset='ultrafast')

        final.close()
        self.video_clip.close()

        return path
    
def zoom_in_effect(clip,mode='in',position='center',speed=23):
    fps = clip.fps
    duration = clip.duration
    total_frames = int(duration*fps)
    def main(getframe,t):
        frame = getframe(t)
        h,w = frame.shape[:2]
        i = t*fps
        if mode == 'out':
            i = total_frames-i
        zoom = 1+(i*((0.1*speed)/total_frames))
        positions = {'center':[(w-(w*zoom))/2,(h-(h*zoom))/2],
                     'left':[0,(h-(h*zoom))/2],
                     'right':[(w-(w*zoom)),(h-(h*zoom))/2],
                     'top':[(w-(w*zoom))/2,0],
                     'topleft':[0,0],
                     'topright':[(w-(w*zoom)),0],
                     'bottom':[(w-(w*zoom))/2,(h-(h*zoom))],
                     'bottomleft':[0,(h-(h*zoom))],
                     'bottomright':[(w-(w*zoom)),(h-(h*zoom))]}
        tx,ty = positions[position]
        M = numpy.array([[zoom,0,tx], [0,zoom,ty]])
        frame = cv2.warpAffine(frame,M,(w,h))
        return frame
    return clip.fl(main)
