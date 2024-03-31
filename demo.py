import streamlit as st

from st_audiorec import st_audiorec


def main():
    with st.sidebar:
        ogg_audio_data = st_audiorec()
        if ogg_audio_data is not None:
            st.audio(ogg_audio_data)

    prompt = st.chat_input("Say something")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)


if __name__ == "__main__":
    main()
