import io
import os
import tempfile

from dotenv import load_dotenv
from pydub import AudioSegment
import openai
import streamlit as st

from st_audiorec import st_audiorec

load_dotenv()


def generate_speech(text):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text,
        )
        response.stream_to_file(temp_file.name)
        temp_file.seek(0)
        audio_bytes = temp_file.read()
    os.remove(temp_file.name)
    return io.BytesIO(audio_bytes)


def transcribe_audio(webm_data):
    client = openai.OpenAI()
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
    view_messages = st.expander("View the message contents in session state")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        webm_audio_data = st_audiorec()

    prompt = st.chat_input("Say something")
    if prompt:
        st.session_state.chat_history.append(("ai", prompt, generate_speech(prompt)))

    if webm_audio_data is not None:
        transcription_text = transcribe_audio(webm_audio_data)
        st.session_state.chat_history.append(
            ("user", transcription_text, webm_audio_data)
        )

    for message_type, message_content, audio_data in st.session_state.chat_history:
        if message_type == "ai":
            with st.chat_message("ai"):
                st.write(message_content)
                st.audio(audio_data, format="audio/mp3")
        elif message_type == "user":
            with st.chat_message("user"):
                st.write(message_content)
                st.audio(audio_data, format="audio/webm")

    view_messages.json([{x[0]: x[1]} for x in st.session_state.chat_history])


if __name__ == "__main__":
    main()
