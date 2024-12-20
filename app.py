import gradio as gr
import os
import re
import csv
import soundfile as sf
import numpy as np

# 設定
SAMPLE_RATE = 44100
OUTPUT_DIR = "output_dataset"
TRANSCRIPTS = "voiceactress100.csv"

# ディレクトリ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# CSVからテキストを読み取る
def load_texts_from_csv(csv_file):
    texts = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
    return texts

# 既存のファイル名から次のインデックスを取得
def get_start_index(output_dir):
    pattern = r"VOICEACTRESS100_([0-9]{4})\.wav"

    # パターンにマッチするファイルを抽出
    existing_files = [
        file_name for file_name in os.listdir(output_dir) if bool(re.search(pattern, file_name))
    ]

    # マッチするファイルがない場合、0を返す
    if not existing_files:
        return 0

    # マッチするファイルのインデックス部分を取得し、最大値を計算
    return max(
        [
            int(re.search(pattern, file_name).group(1)) for file_name in existing_files
        ]
    ) # ファイル名はindex+1であるため、最大値をそのまま返す


# 読み上げるテキストをロード
texts = load_texts_from_csv(TRANSCRIPTS)

# 録音データを保存し、次のテキストに進む
def save_audio(index, audio_data):
    if index >= len(texts):
        return index, "すべてのテキストを読み上げました。", None

    # audio_dataをアンパック
    if isinstance(audio_data, tuple):
        sampling_rate, audio_data = audio_data

    if sampling_rate != SAMPLE_RATE:
        Warning(f"サンプリングレートが{sampling_rate}Hzです。{SAMPLE_RATE}Hzに変換します。")

    # ステレオ音声をモノラルに変換（2次元配列を1次元に）
    if audio_data.ndim == 2:  # ステレオの場合
        audio_data = np.mean(audio_data, axis=1)

    # 録音データを保存
    filename = f"VOICEACTRESS100_{index + 1:04d}.wav"
    filepath = os.path.join(OUTPUT_DIR, filename)
    sf.write(filepath, audio_data, SAMPLE_RATE)

    # 次のテキストを準備
    next_index = index + 1
    next_text = texts[next_index] if next_index < len(texts) else "すべてのテキストを読み上げました。"

    return next_index, f"# {next_index+1}: {next_text}", None

start_index = get_start_index(OUTPUT_DIR)

with gr.Blocks() as demo:
    # UIコンポーネント
    current_text = gr.Markdown("# 現在の読み上げテキスト", elem_id="current_text")
    # https://www.gradio.app/docs/gradio/audio
    audio_input = gr.Audio(
        sources=["microphone"],
        type="numpy",
        label="録音データ",
        show_download_button=True,
        waveform_options=gr.WaveformOptions(sample_rate=SAMPLE_RATE)
        )
    save_button = gr.Button("録音を保存して次へ", variant="primary")
    index_state = gr.State(start_index)

    # 録音保存ボタンの処理
    save_button.click(
        save_audio,
        inputs=[index_state, audio_input],
        outputs=[index_state, current_text, audio_input]
    )

    # 初期状態の更新
    demo.load(
        lambda index: (index, f"# {index+1}: {texts[index]}" if index < len(texts) else "すべてのテキストを読み上げました。", None),
        inputs=index_state,
        outputs=[index_state, current_text, audio_input]
    )

demo.launch()
