import gradio as gr
import os
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

# 読み上げるテキストをロード
texts = load_texts_from_csv(TRANSCRIPTS)

# 録音データを保存し、次のテキストに進む
def save_audio(index, audio_data):
    if index >= len(texts):
        return index, "すべてのテキストを読み上げました。", None

    # audio_dataをアンパック
    if isinstance(audio_data, tuple):
        audio_data, sampling_rate = audio_data

    # サンプリングレートを検証
    if sampling_rate != SAMPLE_RATE:
        Warning(f"サンプリングレートが{SAMPLE_RATE} Hz ではなく{sampling_rate} Hz です。")


    # ステレオ音声をモノラルに変換（2次元配列を1次元に）
    if audio_data.ndim == 2:  # ステレオの場合
        audio_data = np.mean(audio_data, axis=1)

    # 録音データを保存
    filename = f"{index + 1:04d}.wav"
    filepath = os.path.join(OUTPUT_DIR, filename)
    sf.write(filepath, audio_data, SAMPLE_RATE)

    # 次のテキストを準備
    next_index = index + 1
    next_text = texts[next_index] if next_index < len(texts) else "すべてのテキストを読み上げました。"

    return next_index, next_text, filepath

with gr.Blocks() as demo:
    # UIのステート
    index_state = gr.State(0)
    # UIコンポーネント
    current_textbox = gr.Markdown("現在の読み上げテキスト", elem_id="current_textbox")
    audio_input = gr.Audio(sources="microphone", type="numpy", label="録音データ")
    save_button = gr.Button("録音を保存して次へ")

    # CSSでテキストを大きく表示
    demo.css = """
    #current_textbox {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    """

    # 録音保存ボタンの処理
    save_button.click(
        save_audio,
        inputs=[index_state, audio_input],
        outputs=[index_state, current_textbox]
    )

    # 初期状態の更新
    demo.load(
        lambda index: (index, texts[index] if index < len(texts) else "すべてのテキストを読み上げました。", None),
        inputs=index_state,
        outputs=[index_state, current_textbox]
    )

demo.launch()
