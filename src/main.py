import tts, os
from dotenv import load_dotenv
load_dotenv()

session_id = os.getenv("session_id")

def main():

    # Check if our folder for output exists, if not - create
    folder_path = "output"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create audio track
    tts.create(session_id, "en_us_007", "Hello world", os.path.join(folder_path, "voice.mp3"))

if __name__ == '__main__':
    main()