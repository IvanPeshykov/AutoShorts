# YouTube Shorts Automation Tool

This project automates the creation of YouTube Shorts by generating videos with Text-to-Speech (TTS), subtitles, and background music. It allows users to input images and text, which are then transformed into short videos suitable for YouTube Shorts.

# Example

Take a look at [this](https://www.youtube.com/@historioshorts) channel - all of the shorts were created using this tool.
## Features
- **Text-to-Speech Integration**: Supports TTS using either **ElevenLabs** or **TikTok** for generating voiceovers from provided text.
- **Automatic Subtitles Generation**: Subtitles are auto-generated based on the TTS audio output, and users can choose to skip manual subtitle review.
- **Image-to-Video Conversion**: Converts images into videos by adding animated effects and placing the image within a video frame.
- **Background Music**: Option to add background music to the video, enhancing the overall production.
- **Multi-Video Merging**: Combines multiple video clips into a single video output if multiple items are provided.
- **Customizable Output**: Users can specify various settings such as the voice for TTS, audio volume, and whether to keep the original audio in the video.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IvanPeshykov/youtube-shorts-automation.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your **ElevenLabs API key** and **TikTok session ID** (if using TikTok TTS):
   ```env
   elevenlabs_apikey=your_elevenlabs_apikey
   session_id=your_tiktok_session_id
   ```

4. Ensure you have the following external libraries installed:
   - `moviepy`
   - `whisper`
   - `pydub`
   - `requests`
   - `dotenv`

## Configuration

The tool uses a configuration file (`config.json`) to customize the video creation process. Here's an example configuration:

```json
{
  "mode": "manual",
  "tts": "elevenlabs",
  "elevenlabs": {
    "voice_id": "EiNlNiXeDU1pqqOPrYMO"
  },
  "tiktok": {
    "voice_name": "en_us_010"
  },
  "song": "D:/Shorts/assets/music/epic/epic.mp3",
  "skip": true,
  "items": [
    {
      "path": "C:/Users/Ivan/Downloads/tiger.jpg",
      "text": "Why the Tiger1 tank is undoubtedly the best tank ever created?",
      "keep_audio": false
    }
  ]
}
```

### Configuration Parameters:

- **mode**: Defines whether the process is `manual` or `auto`. In manual mode, you can review and edit subtitles before the video is generated.
- **tts**: Choose between `elevenlabs` or `tiktok` for generating voiceovers from text.
- **elevenlabs.voice_id**: The ID of the voice to use for ElevenLabs TTS.
- **tiktok.voice_name**: The name of the voice to use for TikTok TTS.
- **song**: Path to the background music to include in the video.
- **skip**: If set to `true`, the process skips manual subtitle review and proceeds with the video generation automatically.
- **items**: List of items to be processed, where each item includes:
  - `path`: Path to the image to be used in the video.
  - `text`: Text to be converted to speech.
  - `keep_audio`: If `true`, retains the original audio from the video file.

## Usage

1. **Set up the configuration**: Modify the `config.json` file to include your desired settings (TTS voice, image, text, music, etc.).
   
2. **Run the script**:
   ```bash
   python main.py
   ```

3. The script will generate the video, combining the image with the generated voiceover, subtitles, and any provided background music. The final video will be saved to the `output` directory.

4. The generated video will be ready for uploading to YouTube Shorts.

## File Structure

```
.
├── config.json            # Configuration file with settings for the video creation
├── main.py                # Main script for processing the video creation
├── output/                # Directory where the output videos are saved
├── src/                   # Source code files containing the logic for video creation
├── .env                   # Environment variables (API keys, etc.)
└── requirements.txt       # Python dependencies
```

## Dependencies

- `moviepy`: Video editing library to handle video and audio processing.
- `whisper`: For transcribing audio into subtitles.
- `pydub`: For handling audio manipulation (combining and editing).
- `requests`: For making HTTP requests to the TTS APIs.
- `dotenv`: For loading environment variables.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
