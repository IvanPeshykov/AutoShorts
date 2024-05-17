import requests, base64, random, os, whisper, math
from constants import voices, tts_max_characters
from pydub import AudioSegment
from whisper.utils import get_writer
from helpers import format_srt



API_BASE_URL = f"https://api16-normal-v6.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"
session_id = os.environ.get("session_id")

def combine_audios(output_path: str, audios: list[str]):

    combined = AudioSegment.empty()

    for audio in audios:
        combined += AudioSegment.from_file(audio, format="mp3")

    combined_path = os.path.join(output_path, "output.mp3")
    combined.export(combined_path, format="mp3")

    # Delete audios, since we already have combined one
    for audio in audios:
        os.remove(audio)
    
    return combined_path

def tts(session_id : str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech",
        output_path: str = 'output'):
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
    parts = math.ceil(len(req_text) / tts_max_characters)
    temp_audios = []

    for i in range(0, parts):

        r = requests.post(
            f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={req_text[i * tts_max_characters: (i + 1) * tts_max_characters]}&speaker_map_type=0&aid=1233",
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

        path = os.path.join(output_path, "temp" + str(i) + ".mp3")

        with open(os.path.join(output_path, "temp" + str(i) + ".mp3"), "wb") as out:
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

def generate_subtitles(audio_path : str, output_folder = 'output'):
    
    model = whisper.load_model("medium")
    result = model.transcribe(audio_path, language = 'en', word_timestamps=True)
    
    word_options = {
    "highlight_words": False,
    "max_line_count": 1,
    "max_line_width": 10
    }

    output_path = os.path.join(output_folder, output_folder + '.srt')

    vtt_writer = get_writer(output_format='srt', output_dir=output_folder)
    vtt_writer(result, audio_path, word_options)

    format_srt(output_path)

    # Ask user to mannualy continue, because he might want to edit srt file
    input('Press any key to continue')

    return output_path
