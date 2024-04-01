from io import BytesIO
import hashlib
import os

import numpy as np
import streamlit as st
import streamlit.components.v1 as components


def st_audiorec():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)
    raw_audio_data = st_audiorec()

    webm_bytes = None

    if isinstance(raw_audio_data, dict) and "arr" in raw_audio_data:
        # Sort the audio data based on the integer keys
        sorted_audio_data = sorted(
            raw_audio_data["arr"].items(), key=lambda x: int(x[0])
        )

        # Unzip the sorted audio data into separate lists of indices and values
        _, raw_audio_data = zip(*sorted_audio_data)

        # Create a BytesIO stream from the sorted audio data
        sorted_ints = np.array(raw_audio_data, dtype=np.uint8)
        stream = BytesIO(sorted_ints.tobytes())
        webm_bytes = stream.getvalue()

        # Compute the hash of the audio data
        audio_hash = hashlib.sha256(webm_bytes).hexdigest()

        # Check if this hash matches the previous one stored in the session state
        if (
            "st_audiorec_last_audio_hash" in st.session_state
            and st.session_state["st_audiorec_last_audio_hash"] == audio_hash
        ):
            # The audio data hasn't changed
            return None

        # Update the session state with the new audio hash
        st.session_state["st_audiorec_last_audio_hash"] = audio_hash

        return webm_bytes

    return None
