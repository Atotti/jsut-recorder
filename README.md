# VOICEACTRESS100-RECORDER
音声データの収録を楽にするためのアプリケーションです。
ここから下に使い方を説明していきます。

**注意**：Google Cloabは使わないでください。録音したデータが消えます。

## 必要な物
以下の2つが必要になるので、事前にインストールしておいてください。
- [git](https://git-scm.com/)
  - コードをダウンロードするために必要です。便利なのでこれを期に使えるようになるといいです。
  - インストール方法
    - Windowsに入れる場合：[Gitのインストール方法(Windows版)](https://qiita.com/T-H9703EnAc/items/4fbe6593d42f9a844b1c)
    - WLSに入れる場合：`sudo apt-get install git`
  - gitの基本的な使い方：[初心者のためのやさしいGit](https://zenn.dev/getgotgoto/articles/506bcfbcd55149)
- Python3.9以上の環境
  - Pythonのバージョンを確認するには`python -V`を実行してください。
  - [Python3.8は2024年10月にサポートが終了している](https://devguide.python.org/versions/)ので、良い機会と思ってPython3.9以上にアップデートするのが良いでしょう。


## インストール
まずはこのリポジトリをPC内のお好きな場所にクローンします。

このコマンドを実行すると、コマンドを実行した場所に新しく`jsut-recorder`というディレクトリが作成され、その中にこのリポジトリのファイルがダウンロードされます。
```bash
git clone https://github.com/hikuohiku/jsut-recorder.git
```
ここから先のコマンドはクローンしたディレクトリに移動してから実行してください。

次に、必要なライブラリをインストールします。

まず、Pythonの仮想環境を作成します。仮想環境を作成することで、PC内のPythonのバージョンやライブラリのバージョンを気にすることなく、アプリケーションを実行することができます。
```bash
python -m venv .venv
```
次に、作成した仮想環境の中に入ります。[^1]
```bash
source .venv/Scripts/activate
```

[^1]: 仮想環境から抜ける場合は `deactivate` を実行してください。

仮想環境の中に入ったら、以下のコマンドで必要なライブラリをインストールします。これにより、仮想環境の中にライブラリがインストールされます。
```bash
pip install -r requirements.txt
```

## 起動
以下のコマンドでアプリケーションを起動します。仮想環境の中で実行しないとライブラリが無いためエラーが発生します。
```bash
python app.py
```
起動が完了すると、ターミナルに`Running on local URL:  http://127.0.0.1:7860`と表示されるので、http://127.0.0.1:7860 にアクセスしてください。ブラウザ上でアプリケーションが起動しています。

## 使い方





# dev docs

## アプリケーション起動

```bash
uv run app.py
```


## るび付きcsv生成
```bash
uv run ruby.py
```
