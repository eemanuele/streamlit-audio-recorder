import streamlit as st

from st_audiorec import st_audiorec


def main():
    with st.sidebar:
        ogg_audio_data = st_audiorec()

    prompt = st.chat_input("Say something")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

    if ogg_audio_data is not None:
        with st.chat_message("ai"):
            st.audio(ogg_audio_data)


if __name__ == "__main__":
    main()
