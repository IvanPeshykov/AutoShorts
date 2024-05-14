import audio, os, sys
from dotenv import load_dotenv
from video import Video
load_dotenv()

session_id = os.getenv("session_id")
output_path = "output"

def choose_mode(mode : str):
    # -m = manual, -a = automatic
    if mode == '-m':
        video_path = input(str("Specify the path to the video:"))
        
        # Remove quotes (because when you copy path in Windows they are automaticly copied, that's annoing to always remove them manualy)
        video_path = video_path.replace('"', '')

        video_text = input(str("Specify video text:"))

        manual_mode(video_path, video_text)

    elif mode == '-a':
        pass

    else:
        print("You provided invalid mode. Please use -m or -a to launch program")

def manual_mode(video_path : str, video_text : str):
    
    # Create video class
    video = Video(video_path)

    # Create audio track
    voice_path = audio.tts(session_id, "en_au_002", video_text, output_path)
    video.add_audio(voice_path)

    # Create subtitles
    subtitles = audio.generate_subtitles(voice_path, output_path)
    video.add_subtitles(subtitles)

    video.save(os.path.join(output_path, "output.mp4"))


def main():

    # There are 2 modes - manual and automatic. In manual you have to path  and text for the video.
    # In automatic mode you have to just provide video url
    mode = sys.argv[1]

    # Check if our folder for output exists, if not - create

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    choose_mode(mode)

if __name__ == '__main__':
    main()