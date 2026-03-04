import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = None
try:
    client = OpenAI()
except:
    client = None


# ✅ Streamlit cache for Whisper model
@st.cache_resource
def load_whisper_model():
    import whisper
    model = whisper.load_model("base")
    return model


def transcribe_audio(audio_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    try:
        # Try OpenAI API first
        if client:
            try:
                with open(temp_path, "rb") as f:
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=f
                    )
                return transcript.text, 0.9
            except Exception:
                pass

        # ✅ fallback to cached Whisper
        model = load_whisper_model()
        result = model.transcribe(temp_path)

        return result["text"], 0.75

    finally:
        os.remove(temp_path)