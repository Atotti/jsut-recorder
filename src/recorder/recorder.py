import sounddevice as sd
import numpy as np
import wave

def record_audio(output_file, duration=5, samplerate=44100, channels=2):
    """
    Record audio and save it to a file.

    Parameters:
        output_file (str): Path to the output WAV file.
        duration (int): Duration of the recording in seconds. Default is 5 seconds.
        samplerate (int): Sampling rate for the recording. Default is 44100 Hz.
        channels (int): Number of audio channels. Default is 2 (stereo).

    Returns:
        None
    """
    try:
        print(f"Recording audio for {duration} seconds...")
        # Record audio
        audio_data = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=channels,
            dtype=np.int16
        )
        sd.wait()  # Wait for the recording to finish

        print(f"Saving audio to {output_file}...")
        # Save audio to a WAV file
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(np.dtype(np.int16).itemsize)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())

        print("Recording saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
def main():
    output_file = "output.wav"
    duration = 5  # Record for 5 seconds
    record_audio(output_file, duration)

if __name__ == "__main__":
    main()

