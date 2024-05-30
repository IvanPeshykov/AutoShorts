import os, argparse, multiprocessing, json
from src import audio
from src.video import Video
from dotenv import load_dotenv
from src.helpers import format_song
load_dotenv()

session_id = os.getenv("session_id")
output_path = "output"

def choose_mode(data):

    if data['mode'] == 'manual':

        if len(data['items']) == 0:
            print('Please, provide at least 1 video!')
            return    

        create_videos(data)

    elif data['mode'] == 'auto':
        pass

    else:
        print("You provided invalid mode. Please choose valid mode")

def combine_videos(videos):

    if len(videos) == 1:
        return videos[0]
    
    return Video.combine_videos(videos)

def create_video(item, voice_path, subtitles, index):

    # Create video class
    video = Video(item['path'])

    # Crop video and add transparent images
    video.video_clip = video.crop_video(video.video_clip, 40)
    video = video.add_images(video.video_clip, 30)

    # Add subtitles track
    video.add_audio(voice_path)

    # Add subtitles
    video.add_subtitles(subtitles)

    video_path = video.save(os.path.join(output_path, "output" + str(index) + ".mp4"))

    return video_path
    

def create_videos(data):

    subtitles_audio = []
    subtitles = []

    for i, item in enumerate(data['items']):

        voice_output_path = os.path.join(output_path, 'output' + str(i) + '.mp3')
        voice_path = ''

        # Create subtitles track
        
        if data['tts'] == 'elevenlabs':
            voice_path = audio.elevenlabs_tts(item['text'], data['elevenlabs']['voice_id'], voice_output_path)

        else:
            voice_path = audio.tiktok_tts(session_id, i, data['tiktok']['voice_name'], item['text'], voice_output_path)
            
        subtitles_audio.append(voice_path)

        # Create subtitles
        subtitles.append(audio.generate_subtitles(voice_path, output_path, data['skip']))
    
    # Ask user to mannualy continue, because he might want to edit srt file
    if not data['skip']:
        input('Press any key to continue')

    args = [(video, subtitles_audio[index], subtitles[index], index) for  index, video in enumerate(data['items'])]

    
    # Determine the number of worker processes to use
    num_workers = min(len(data['items']), multiprocessing.cpu_count())
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_workers) as pool:
        # Use starmap to pass multiple arguments to the worker function
        results = pool.starmap(create_video, args)

    combined_video = combine_videos([Video(result) for  result in results])

     # Create song track (if needed)
    if data['song'] != '':
       combined_video.add_audio(format_song(data['song']), 0.1)

    combined_video.save(os.path.join(output_path, "output.mp4"), True)

def main():

    with open('config.json') as config:
        data = json.load(config)

    # Check if our folder for output exists, if not - create
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Clear output folder
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    choose_mode(data)

if __name__ == '__main__':
    main()