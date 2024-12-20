import csv

import MeCab
from pykakasi import kakasi

tagger = MeCab.Tagger()
kks = kakasi()


# 入力CSVファイル
input_csv = "voiceactress100.csv"
# 出力CSVファイル（ルビ付き）
output_csv = "voiceactress100_with_ruby.csv"

def convert(text):
    return "".join([tmp['hira'] for tmp in kks.convert(text)])

# https://github.com/getuka/RubyInserter を参考に拡張を加えた
def add_ruby(text:str ) -> str:
    """Add ruby to the text.

    Args:
        text (str): Text to add ruby.
        ex. "石炭の積み込みがもう終わった。"

    Returns:
        str: Text with ruby, html format.
        ex. "石炭<ruby>せきたん<rt>せきたん</rt></ruby>の積み込み<ruby>つみこみ<rt>つみこみ</rt></ruby>がもう終わった<ruby>おわった<rt>おわった</rt></ruby>。"
    """
    parsed_text = tagger.parse(text)

    # 結果を行ごとに分割
    lines = parsed_text.splitlines()

    replaced_text = []
    for line in lines:
        # 行が形態素解析の結果である場合のみ処理する
        if '\t' in line:
            parts = line.split('\t')

            if parts[1] == "":
                if convert(parts[3]) == parts[0]:
                    replaced_text.append(parts[0])
                else:
                    replaced_text.append(f"<ruby>{parts[0]}<rt>{convert(parts[3])}</rt></ruby>")
            else:
                if (convert(parts[2]) == parts[0]) or (convert(parts[1]) == parts[0]):
                    replaced_text.append(parts[0])
                else:
                    replaced_text.append(f"<ruby>{parts[0]}<rt>{convert(parts[1])}</rt></ruby>")

    return "".join(replaced_text)


with open(input_csv, newline='', encoding="utf-8") as infile, open(output_csv, mode="w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["ruby_text"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row["ruby_text"] = add_ruby(row["text"])
        writer.writerow(row)

print(f"ルビ付きCSVを {output_csv} に保存しました。")
