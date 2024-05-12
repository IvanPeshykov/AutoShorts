import tts, os, argparse
from dotenv import load_dotenv
from video import Video
load_dotenv()

session_id = os.getenv("session_id")

def main():

    parser = argparse.ArgumentParser("AutoShorts")
    parser.add_argument("path", help="Path of the video")
    args = parser.parse_args()

    # Check if our folder for output exists, if not - create
    folder_path = "output"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create video class

    video = Video(args.path)

    # Create audio track
    voice_path = tts.create(session_id, "en_us_007", "Hello world", os.path.join(folder_path, "voice.mp3"))
    video.add_audio(voice_path)

    video.save(os.path.join(folder_path, "output.mp4"))

if __name__ == '__main__':
    main()