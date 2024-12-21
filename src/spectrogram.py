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

    os.makedirs("tmp_img", exist_ok=True)

    plt.savefig(f"tmp_img/{user_name}.png")
    plt.close()  # メモリ解放

    return f"tmp_img/{user_name}.png"
