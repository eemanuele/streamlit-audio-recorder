import io
import os
import tempfile

from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
import streamlit as st

from st_audiorec import st_audiorec

load_dotenv()


def transcribe_audio(webm_data):
    client = OpenAI()
    audio_segment = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        audio_segment.export(temp_file.name, format="mp3")
        with open(temp_file.name, "rb") as audio_file:
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="Hello, welcome to my lecture.",
            )
        os.remove(temp_file.name)
    return transcription_response.text


def main():
    with st.sidebar:
        webm_audio_data = st_audiorec()

    prompt = st.chat_input("Say something")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

    if webm_audio_data is not None:
        with st.chat_message("ai"):
            st.audio(webm_audio_data, format="audio/webm")
            transcription_text = transcribe_audio(webm_audio_data)
            st.write(transcription_text)


if __name__ == "__main__":
    main()
