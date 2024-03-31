import os
from io import BytesIO

import numpy as np
import streamlit.components.v1 as components


def st_audiorec():
    # Get the parent directory relative to the current file's location
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the build directory of the custom REACT-based audio recording component
    build_dir = os.path.join(parent_dir, "frontend/build")
    # Declare the Streamlit component with its frontend build directory
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # Create an instance of the audio recorder component
    raw_audio_data = st_audiorec()  # Stores all the data returned from the frontend

    # Initialize variable to hold the processed audio data
    webm_bytes = None

    # Check if the frontend returned audio data in the expected format
    if isinstance(raw_audio_data, dict) and "arr" in raw_audio_data:
        # Unpack the dictionary items and sort them based on the keys to ensure correct order
        ind, raw_audio_data = zip(*raw_audio_data["arr"].items())
        ind = np.array(ind, dtype=int)  # Convert keys to a numpy array for indexing
        raw_audio_data = np.array(raw_audio_data)  # Convert values to a numpy array
        sorted_ints = raw_audio_data[ind]  # Reorder the array based on the keys
        # Create a bytes stream from the ordered integers
        stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
        webm_bytes = stream.read()  # Read the bytes stream into a bytes object

    # Return the audio data in WebM format with Opus codec
    return webm_bytes
