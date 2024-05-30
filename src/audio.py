import requests, base64, random, os, whisper, math
from src.constants import voices, tts_max_characters
from pydub import AudioSegment
from whisper.utils import get_writer
from src.helpers import format_srt



elevenlabs_apikey = os.environ.get("elevenlabs_apikey")
session_id = os.environ.get("session_id")

def combine_audios(output_path: str, audios: list[str]):

    combined = AudioSegment.empty()

    for audio in audios:
        combined += AudioSegment.from_file(audio, format="mp3")

    combined.export(output_path, format="mp3")

    # Delete audios, since we already have combined one
    for audio in audios:
        os.remove(audio)
    
    return output_path

def split_text(text):
     
    parts = []
    temp_str = ''
    counter = 0

    for c in text:
        temp_str += c
        counter += 1

        if c == '.' or counter >= tts_max_characters:
            parts.append(temp_str)
            counter = 0
            temp_str = ''
    
    if len(temp_str) > 0:
            parts.append(temp_str)
    
    return parts

def elevenlabs_tts(text : str = 'Elvenlabs text to speech', voice_id = '', output_path = 'output.mp3'):

    chunck_size = 1024  # Size of chunks to read/write at a time

    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    
    # Set up headers for the API request, including the API key for authentication
    headers = {
    "Accept": "application/json",
    "xi-api-key": elevenlabs_apikey
    }
    
    # Set up the data payload for the API request, including the text and voice settings
    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
        }
    }
    
    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)
    
    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(output_path, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=chunck_size):
                f.write(chunk)

        return output_path
    
    else:
        # Raise the error message if the request was not successful
         raise ValueError(response.text)


def tiktok_tts(session_id : str, index,  text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech",
        output_path: str = 'output.mp3'):

    API_BASE_URL = f"https://api16-normal-v6.tiktokv.com/media/api/text/speech/invoke/"
    USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    req_text = req_text.replace("ä", "ae")
    req_text = req_text.replace("ö", "oe")
    req_text = req_text.replace("ü", "ue")
    req_text = req_text.replace("ß", "ss")

    if text_speaker == "random":
        text_speaker = randomvoice()

    # Tiktok tts api accepts only 300 characters per one call. So we will make multiple calls if needed and merge audio
    parts = split_text(req_text)
    temp_audios = []  
    

    for i, text in enumerate(parts):

        r = requests.post(
            f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={text}&speaker_map_type=0&aid=1233",
            headers={
            'User-Agent': USER_AGENT,
            'Cookie': f'sessionid={session_id}'
            }
        )

        if r.json()["message"] == "Couldn’t load speech. Try again.":
            output_data = {"status": "Session ID is invalid", "status_code": 5}
            print(output_data)
            return output_data

        vstr = [r.json()["data"]["v_str"]][0]
        msg = [r.json()["message"]][0]
        scode = [r.json()["status_code"]][0]
        log = [r.json()["extra"]["log_id"]][0]

        dur = [r.json()["data"]["duration"]][0]
        spkr = [r.json()["data"]["speaker"]][0]

        b64d = base64.b64decode(vstr)

        path = "temp" + str(index) + str(i) + ".mp3"

        with open(path, "wb") as out:
            out.write(b64d)
            temp_audios.append(path)

        output_data = {
            "status": msg.capitalize(),
            "status_code": scode,
            "duration": dur,
            "speaker": spkr,
            "log": log
        }

    combined_path = combine_audios(output_path, temp_audios)
    
    return combined_path


def randomvoice():
    count = random.randint(0, len(voices))
    text_speaker = voices[count]

    return text_speaker

def generate_subtitles(audio_path : str, output_folder = 'output', skip = False):
    
    model = whisper.load_model("medium")
    result = model.transcribe(audio_path, language = 'en', word_timestamps=True)
    
    word_options = {
    "highlight_words": False,
    "max_line_count": 1,
    "max_line_width": 10
    }

    output_path = audio_path[:-4] + '.srt'

    vtt_writer = get_writer(output_format='srt', output_dir=output_folder)
    vtt_writer(result, audio_path, word_options)

    format_srt(output_path)

    return output_path
