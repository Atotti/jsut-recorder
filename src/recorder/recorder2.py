import sounddevice as sd
import numpy as np
import wave
import threading

class AudioRecorder:
    def __init__(self, output_file, samplerate=44100, channels=2):
        self.output_file = output_file
        self.samplerate = samplerate
        self.channels = channels
        self.recording = False
        self.audio_data = []

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data.append(indata.copy())

    def start(self):
        """Start recording."""
        self.recording = True
        self.audio_data = []
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback,
            dtype=np.int16
        )
        self.stream.start()
        print("Recording started. Press Ctrl+C to stop.")

    def stop(self):
        """Stop recording and save to a WAV file."""
        self.recording = False
        self.stream.stop()
        self.stream.close()
        print("Recording stopped. Saving audio...")

        # Combine recorded data
        audio_array = np.concatenate(self.audio_data, axis=0)

        # Save to WAV file
        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(np.dtype(np.int16).itemsize)
            wf.setframerate(self.samplerate)
            wf.writeframes(audio_array.tobytes())

        print(f"Audio saved to {self.output_file}")

def main():
    output_file = "output.wav"
    recorder = AudioRecorder(output_file)

    try:
        recorder.start()
        while True:
            pass  # Keep the program running
    except KeyboardInterrupt:
        recorder.stop()
        print("Exiting program.")

if __name__ == "__main__":
    main()

