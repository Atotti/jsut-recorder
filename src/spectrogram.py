import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

def show_spectrogram(audio: np.ndarray) -> str:
    frequencies, times, Sxx = spectrogram(audio, 44100)
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [s]")
    plt.colorbar(label="Intensity [dB]")
    plt.tight_layout()

    plt.savefig("tmp_spectrogram.png")

    return "tmp_spectrogram.png"
