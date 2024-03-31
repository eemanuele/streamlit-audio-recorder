import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components


def st_audiorec():
    # get parent directory relative to current directory
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "frontend/build")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # Create an instance of the component: STREAMLIT AUDIO RECORDER
    raw_audio_data = (
        st_audiorec()
    )  # raw_audio_data: stores all the data returned from the streamlit frontend
    ogg_bytes = None

    # the frontend returns raw audio data in the form of arraybuffer
    # (this arraybuffer is derived from web-media API WAV-blob data)

    if isinstance(raw_audio_data, dict) and "arr" in raw_audio_data:
        ind, raw_audio_data = zip(*raw_audio_data["arr"].items())
        ind = np.array(ind, dtype=int)  # convert to np array
        raw_audio_data = np.array(raw_audio_data)  # convert to np array
        sorted_ints = raw_audio_data[ind]
        stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
        # ogg_bytes contains audio data in byte format, ready to be processed further
        ogg_bytes = stream.read()

    return ogg_bytes
