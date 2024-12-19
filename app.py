import gradio as gr
import sounddevice as sd
import librosa
import numpy as np
import csv
import os
import soundfile as sf
import io

# 設定
SAMPLE_RATE = 44100
OUTPUT_DIR = "output_dataset"
METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata.csv")

# ディレクトリ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 無音検出と音声分割
def split_audio(audio_path, threshold=-40, min_silence_duration=0.3):
    y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    intervals = librosa.effects.split(y, top_db=threshold, frame_length=int(sr * min_silence_duration))
    audio_clips = []
    for i, (start, end) in enumerate(intervals):
        audio_clips.append((y[start:end], sr))  # サンプリングレートも保持
    return audio_clips

def record_audio(seconds):
    myrecording = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    return myrecording.flatten()  # 1次元配列に変換

def create_dataset(texts, recorded_audio):
    if not recorded_audio:
        return "エラー: 録音データがありません。"
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, recorded_audio, SAMPLE_RATE, format="WAV")
    audio_buffer.seek(0)
    clips = split_audio(audio_buffer)

    metadata = []
    for i, (clip, sr) in enumerate(clips):
        if i < len(texts):
            filename = os.path.join(OUTPUT_DIR, f"{i+1:04d}.wav")
            sf.write(filename, clip, sr, format="WAV")
            metadata.append([f"{i+1:04d}.wav", texts[i]])
        else:
            break

    # metadata.csvへの書き込み
    with open(METADATA_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_name", "text"])
        writer.writerows(metadata)
    return metadata

def preview_audio(filename):
    if filename:
        full_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(full_path):
            return full_path
    return None

with gr.Blocks() as demo:
    text_input = gr.Textbox(label="読み上げるテキスト（改行区切り）", lines=5)
    record_time_slider = gr.Slider(minimum=1, maximum=10, value=5, step=1, label="録音時間（秒）")
    record_button = gr.Button("録音開始")
    recorded_audio_output = gr.Audio(label="録音データ", type="numpy")
    dataset_button = gr.Button("データセット作成")
    metadata_output = gr.DataFrame(headers=["file_name", "text"], label="生成されたデータセット")
    preview_dropdown = gr.Dropdown(label="プレビューする音声ファイル", allow_custom_value=False)
    preview_audio_output = gr.Audio(label="音声プレビュー")

    record_button.click(record_audio, inputs=record_time_slider, outputs=recorded_audio_output)

    dataset_button.click(
        create_dataset,
        inputs=[text_input, recorded_audio_output],
        outputs=metadata_output
    )
    dataset_button.click(
        lambda: [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".wav")],
        outputs=preview_dropdown
    )

    preview_dropdown.change(preview_audio, inputs=preview_dropdown, outputs=preview_audio_output)

demo.launch()
