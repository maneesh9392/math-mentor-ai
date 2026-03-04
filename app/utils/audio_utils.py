import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv
import whisper

load_dotenv()

client = None
try:
    client = OpenAI()
except:
    client = None

# Load local whisper model once
local_model = whisper.load_model("base")


def transcribe_audio(audio_file):
    """
    Tries OpenAI API first.
    Falls back to local Whisper if quota exceeded.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    try:
        # ======================
        # Try OpenAI API
        # ======================
        if client:
            try:
                with open(temp_path, "rb") as f:
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=f
                    )

                return transcript.text, 0.9
            except Exception:
                pass  # fallback to local

        # ======================
        # Local Whisper fallback
        # ======================
        result = local_model.transcribe(temp_path)
        return result["text"], 0.75

    finally:
        os.remove(temp_path)