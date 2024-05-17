import audio, os, argparse
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
        video_path = input(str("Specify the path to the video:"))
        
        # Remove quotes (because when you copy path in Windows they are automaticly copied, that's annoing to always remove them manualy)
        video_path = video_path.replace('"', '')

        video_text = input(str("Specify video text:"))

        manual_mode(video_path, video_text, args.s)

    elif args.mode == 'a':
        pass

    else:
        print("You provided invalid mode. Please choose valid mode")

def manual_mode(video_path : str, video_text : str, song : str):
    
    # Create video class
    video = Video(video_path)

    # Create subtitles track
    voice_path = audio.tts(session_id, "en_au_002", video_text, output_path)
    video.add_audio(voice_path)

    # Create song track (if needed)
    if song != '':
        video.add_audio(song, 0.15)

    # Create subtitles
    subtitles = audio.generate_subtitles(voice_path, output_path)
    video.add_subtitles(subtitles)

    video.save(os.path.join(output_path, "output.mp4"))


def main():

    parser = argparse.ArgumentParser('AutoShorts')
    # There are 2 modes - manual and automatic. In manual you have to path  and text for the video.
    # In automatic mode you have to just provide video url
    parser.add_argument('mode', default='m', choices=['m', 'a'], help='Parser mode')
    # Song is an optional argument, it is either pat to file or to folder
    parser.add_argument('--s', '--path', required=False, default='')
    args = parser.parse_args()

    
    # Check if our folder for output exists, if not - create

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    choose_mode(args)

if __name__ == '__main__':
    main()