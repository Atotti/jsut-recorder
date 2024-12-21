import gradio as gr
import os
import re
import csv
import soundfile as sf
import numpy as np

from src.spectrogram import show_spectrogram

# 設定
SAMPLE_RATE = 44100
OUTPUT_DIR = "output_dataset"
TRANSCRIPTS = "voiceactress100_with_ruby.csv"

# ディレクトリ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# CSVからテキストを読み取る
def load_texts_from_csv(csv_file):
    texts = []
    hira_texts = []
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["ruby_text"]) # ルビ付きテキストを読み込む
            hira_texts.append(row["text"])
    return texts, hira_texts

# 既存のファイル名から次のインデックスを取得
def get_start_index(user_dir):
    pattern = r"VOICEACTRESS100_([0-9]{4})\.wav"

    os.makedirs(user_dir, exist_ok=True)


    # パターンにマッチするファイルを抽出
    existing_files = [
        file_name for file_name in os.listdir(user_dir) if bool(re.search(pattern, file_name))
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
texts, hira_texts = load_texts_from_csv(TRANSCRIPTS)

# ユーザー音声ファイル一覧
def get_audio_list(user_name):
    if isinstance(user_name, gr.State):
        user_name = user_name.value  # Stateから値を取得
    if not isinstance(user_name, str) or user_name == "":
        return []

    pattern = r"VOICEACTRESS100_([0-9]{4})\.wav"
    user_dir = os.path.join(OUTPUT_DIR, user_name)
    os.makedirs(user_dir, exist_ok=True)
    files = [file_name + "(" + hira_texts[int(re.search(pattern, file_name).group(1)) - 1] + ")" for file_name in os.listdir(user_dir) if bool(re.search(pattern, file_name))]
    return files if files else ["録音済みの音声はありません"]


# 音声再録音
def rerecord_audio(selected_file, now_index, user_name):
    selected_file = selected_file.split("(")[0]
    index = int(re.search(r"VOICEACTRESS100_([0-9]{4})\.wav", selected_file).group(1)) - 1

    return index, f"<h1>{index+1}: {texts[index]}</h1>"


# 最新の発話に戻る
def return_to_latest(user_name):
    user_dir = os.path.join(OUTPUT_DIR, user_name)
    os.makedirs(user_dir, exist_ok=True)
    latest_index = get_start_index(user_dir)
    return latest_index, f"<h1>{latest_index+1}: {texts[latest_index]}</h1>", None,


def save_audio(index, audio_data, spectrogram_visibility, user_name):
    if index >= len(texts):
        return index, "すべてのテキストを読み上げました。", None, None, user_name, gr.update(choices=get_audio_list(user_name))

    if audio_data is None:
        gr.Warning("先に録音を完了してください。")
        return index, f"<h1>{index+1}: {texts[index]}</h1>", None, None, user_name, gr.update(choices=get_audio_list(user_name))

    if user_name == "":
        gr.Warning("ログインしてください。")
        return index, f"<h1>{index+1}: {texts[index]}</h1>", None, None, user_name, gr.update(choices=get_audio_list(user_name))

    # audio_dataをアンパック
    if isinstance(audio_data, tuple):
        sampling_rate, audio_data = audio_data

    if sampling_rate != SAMPLE_RATE:
        gr.Warning(f"サンプリングレートが{sampling_rate}Hzです。{SAMPLE_RATE}Hzに変換します。")

    # ステレオ音声をモノラルに変換（2次元配列を1次元に）
    if audio_data.ndim == 2:  # ステレオの場合
        audio_data = np.mean(audio_data, axis=1)

    # 録音データを保存
    user_dir = os.path.join(OUTPUT_DIR, user_name)
    filename = f"VOICEACTRESS100_{index + 1:04d}.wav"
    filepath = os.path.join(user_dir, filename)
    sf.write(filepath, audio_data, SAMPLE_RATE)

    # 次のテキストを準備
    next_index = index + 1
    next_text = texts[next_index] if next_index < len(texts) else "すべてのテキストを読み上げました。"

    spectrogram_output = show_spectrogram(audio_data, user_name) if spectrogram_visibility else None

    return next_index, f"<h1>{next_index+1}: {next_text}</h1>", None, spectrogram_output, user_name, gr.update(choices=get_audio_list(user_name))


def toggle_spectrogram_visibility(state):
    state = not state
    return state, ("スペクトログラムを非表示にする" if state else "スペクトログラムを表示する"), gr.update(visible=state)


# ログイン処理
def login(user_name):
    user_dir = os.path.join(OUTPUT_DIR, user_name)
    start_index = get_start_index(user_dir)
    return user_name, gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), f"現在のユーザー：{user_name}", \
        f"<h1>{start_index+1}: {texts[start_index]}</h1>", gr.update(visible=True), gr.update(visible=True), \
        gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), \
        gr.update(visible=True), gr.update(visible=True), gr.update(choices=get_audio_list(user_name))

with gr.Blocks() as demo:
    index_state = gr.State(0)
    spectrogram_visibility = gr.State(True)
    user_name = gr.State("")
    # UIコンポーネント

    login_name = gr.Textbox(label="名前を入力してログイン", placeholder="例）ayuto", visible=True)
    login_button = gr.Button("ログイン", visible=True)
    user_name_display = gr.Markdown("", visible=False)

    current_text = gr.Markdown("<h1>現在の読み上げテキスト</h1>", elem_id="current_text", visible=False)
    # https://www.gradio.app/docs/gradio/audio
    audio_input = gr.Audio(
        sources=["microphone"],
        type="numpy",
        label="録音データ",
        show_download_button=True,
        waveform_options=gr.WaveformOptions(sample_rate=SAMPLE_RATE),
        visible=False,
        )
    save_button = gr.Button("録音を保存して次へ", variant="primary", visible=False,)
    spectrogram_toggle_button = gr.Button("スペクトログラムを非表示にする", variant="secondary", visible=False)
    spectrogram_output = gr.Image(label="スペクトログラム", type="numpy", visible=False)
    audio_list = gr.Dropdown(label="録音済み音声一覧", choices=[], visible=False)
    rerecord_button = gr.Button("選択した音声を再録音する", visible=False)
    latest_button = gr.Button("最新の発話に戻る", visible=False)

    # ログイン処理
    login_button.click(
        login,
        inputs=login_name,
        outputs=[
            user_name,  # ユーザー名更新
            login_name,  # ログイン後非表示
            login_button,  # ログイン後非表示
            user_name_display,  # ログイン後表示
            user_name_display,  # ユーザー名表示更新
            current_text,  # 現在のテキスト表示
            current_text, # ログイン後表示
            audio_input,  # 録音UI表示
            save_button,  # 保存ボタン表示
            spectrogram_toggle_button,  # スペクトログラム表示ボタン表示
            spectrogram_output, # スペクトログラム表示
            audio_list, # 音声ファイル一覧表示
            rerecord_button, # 再録音ボタン表示
            latest_button, # 最新の発話に戻るボタン表示
            audio_list, # 音声ファイル一覧表示
        ],
    )

    rerecord_button.click(
        rerecord_audio,
        inputs=[audio_list, index_state, user_name],
        outputs=[index_state, current_text]
    )

    latest_button.click(
        return_to_latest,
        inputs=user_name,
        outputs=[index_state, current_text, audio_list]
    )

    spectrogram_toggle_button.click(
        toggle_spectrogram_visibility,
        inputs=spectrogram_visibility,
        outputs=[spectrogram_visibility, spectrogram_toggle_button, spectrogram_output]
    )

    # 録音保存ボタンの処理
    save_button.click(
        save_audio,
        inputs=[index_state, audio_input, spectrogram_visibility, user_name],
        outputs=[index_state, current_text, audio_input, spectrogram_output, user_name, audio_list]
    )

    # 初期状態の更新
    demo.load(
        lambda index: (index, f"<h1>{index+1}: {texts[index]}</h1>" if index < len(texts) else "すべてのテキストを読み上げました。", None, None, get_audio_list(user_name)),
        inputs=index_state,
        outputs=[index_state, current_text, audio_input, spectrogram_output, audio_list]
    )

    demo.css = """
    #ruby-text ruby rt {
        font-size: 0.8em;
        color: gray;
    }
    """


demo.launch()
