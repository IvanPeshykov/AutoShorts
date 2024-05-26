import audio, os, argparse, multiprocessing
from video import Video
from dotenv import load_dotenv
from helpers import format_song
load_dotenv()

session_id = os.getenv("session_id")
output_path = "output"

def choose_mode(args):

    args.s = format_song(args.s)

    # -m = manual, -a = automatic
    if args.mode == 'm':

        items = []

        while(True):
            video_path = input(str("Specify the path to the video: (leave empty to continue)" ))

            if video_path == '':
                break
        
            # Remove quotes (because when you copy path in Windows they are automaticly copied, that's annoing to always remove them manualy)
            video_path = video_path.replace('"', '')

            video_text = input(str("Specify video text:"))

            items.append({'path' : video_path.strip(), 'text' : video_text.strip()})

        if len(items) == 0:
            print('Please, provide at least 1 video!')
            return    

        create_videos(items, args.s, args.skip)

    elif args.mode == 'a':
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
    

def create_videos(videos, song : str, skip):

    subtitles_audio = []
    subtitles = []

    for i, item in enumerate(videos):
        # Create subtitles track
        voice_path = audio.tts(session_id, i, "en_us_010", item['text'], os.path.join(output_path, 'output' + str(i) + '.mp3'))

        subtitles_audio.append(voice_path)

        # Create subtitles
        subtitles.append(audio.generate_subtitles(voice_path, output_path, skip))
    
    # Ask user to mannualy continue, because he might want to edit srt file
    if not skip:
        input('Press any key to continue')

    args = [(video, subtitles_audio[index], subtitles[index], index) for  index, video in enumerate(videos)]

    
    # Determine the number of worker processes to use
    num_workers = min(len(videos), multiprocessing.cpu_count())
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_workers) as pool:
        # Use starmap to pass multiple arguments to the worker function
        results = pool.starmap(create_video, args)

    combined_video = combine_videos([Video(result) for  result in results])

     # Create song track (if needed)
    if song != '':
       combined_video.add_audio(song, 0.1)

    combined_video.save(os.path.join(output_path, "output.mp4"), True)

def main():

    parser = argparse.ArgumentParser('AutoShorts')
    # There are 2 modes - manual and automatic. In manual you have to path  and text for the video.
    # In automatic mode you have to just provide video url
    parser.add_argument('mode', default='m', choices=['m', 'a'], help='Parser mode')
    # Song is an optional argument, it is either pat to file or to folder
    parser.add_argument('--s', '--path', required=False, default='')
    # Argument for automatic skip of requesting user to press any key 
    parser.add_argument('-a', '--skip', action='store_true', help='Automatic skip flag')
    args = parser.parse_args()

    # Check if our folder for output exists, if not - create

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Clear output folder
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    choose_mode(args)

if __name__ == '__main__':
    main()