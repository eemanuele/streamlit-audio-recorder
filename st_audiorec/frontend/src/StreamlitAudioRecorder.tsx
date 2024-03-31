import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

declare var MediaRecorder: any;
declare var Blob: any;

interface MediaRecorder {
  new (stream: MediaStream): MediaRecorder;
  start(): void;
  stop(): void;
  state: 'inactive' | 'recording' | 'paused';
  addEventListener(event: 'dataavailable' | 'stop', callback: (event: any) => void): void;
}

interface Window {
  MediaRecorder: typeof MediaRecorder;
}

interface State {
  isRecording: boolean;
  audioDataURL: string;
}

class StAudioRec extends StreamlitComponentBase<State> {
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];

  public state = { isRecording: false, audioDataURL: "" };

  public render = (): ReactNode => {
    const { isRecording } = this.state;
    return (
      <span>
        <button onClick={this.toggleRecording}>
          {isRecording ? (
            <span>&#9632;</span> // Stop symbol
          ) : (
            <span>&#127908;</span> // Microphone symbol
          )}
        </button>
      </span>
    );
  };

  private toggleRecording = async () => {
    const { isRecording } = this.state;
    if (isRecording) {
      this.stopRecording();
    } else {
      await this.startRecording();
    }
  };

  private startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];

      this.mediaRecorder.addEventListener("dataavailable", (event) => {
        this.audioChunks.push(event.data);
      });

      this.mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
        const audioDataURL = URL.createObjectURL(audioBlob);
        this.setState({ audioDataURL });

        audioBlob.arrayBuffer().then((buffer) => {
          Streamlit.setComponentValue({
            arr: new Uint8Array(buffer),
          });
        });
      });

      this.mediaRecorder.start();
      this.setState({ isRecording: true });
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  };

  private stopRecording = () => {
    if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
      this.mediaRecorder.stop();
      this.setState({ isRecording: false });
    }
  };
}

export default withStreamlitConnection(StAudioRec);
Streamlit.setComponentReady();
Streamlit.setFrameHeight();
