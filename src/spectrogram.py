import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import os

def show_spectrogram(audio: np.ndarray, user_name: str) -> str:
    frequencies, times, Sxx = spectrogram(audio, 44100)
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [s]")
    plt.colorbar(label="Intensity [dB]")
    plt.tight_layout()

    if not os.path.exists(user_name):
        os.makedirs(user_name)

    plt.savefig(f"{user_name}/tmp_spectrogram.png")

    return f"{user_name}/tmp_spectrogram.png"
