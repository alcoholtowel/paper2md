import openai
import tiktoken
import sys
from pix2text import Pix2Text

sys.stdout.reconfigure(encoding='utf-8')

# 使い方

# Python translate.py (入力ファイル) (出力してほしい名前.md) で実行
# pdfなら勝手にOCRして、md/textならさっそく翻訳します

# 自分で設定してほしい箇所
openai.api_key = 'ここにapi_keyを貼り付け'

# プロンプト改変したい場合はどうぞ
prompt = "あなたは翻訳ツールです。翻訳内容以外の文章は決して出力しないでください。インライン数式は[$, $]で、ブロック数式は[$$, $$]で囲われています。科学的専門用語、人名は英語表記でお願いします。この表記を変更しないでください。入力された文章を日本語で意訳しなさい。"

# モデルごとの単価 4o以外を使う場合は編集してください。
input_price = 0.000005   # $5 / 1M
output_price = 0.000015  # $15 / 1M


def text2jp(text):
	if len(text) <= 5:
		return text
	if text.startswith("[$") and text.endswith("$]"):
		return text
	
	response = openai.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content":prompt},
			{"role": "user", "content": text}
		],
	)

	return response.choices[0].message.content

def split_paragraphs(text):
	return [p.strip() for p in text.split("\n\n") if p.strip()]

def get_token(text):
	enc = tiktoken.get_encoding("o200k_base")
	tokens = enc.encode(text)
	return len(tokens)

def estimated_fee(input_tokens):

	estimated_output_tokens = int(input_tokens * 1.15)
	cost = input_tokens * input_price + estimated_output_tokens * output_price

	print(f"概算：入力 {input_tokens:,} tokens、出力 約 {estimated_output_tokens:,} tokens", flush=True)
	print(f"想定コスト：約 ${cost:.2f} USD", flush=True)
	return

def pdf2markdown(path):

	p2t = Pix2Text.from_config(enable_table=False)
	print("=== OCR処理を開始 ===")
	doc = p2t.recognize_pdf(path)
	
	doc.to_markdown("./output")
	print("=== PDFがmarkdownに変換されました ===")

	return

def remove_figures_prefix(md_text):
	# Windows用のバックスラッシュに注意（\\でエスケープ）
	return re.sub(r'!\[\]\(figures\\', '![](', md_text)

def main():
		input_path = sys.argv[1]
	output_path = sys.argv[2]

	# pdfのファイル名を入力された場合
	if input_path.lower().endswith('.pdf'):
		print("=== PDFが入力されました ===")
		pdf2markdown(input_path)
		# マークダウン化して対象パスを変更
		input_path = "output/output.md"

	# 選択されたファイルを読み込み
	with open(input_path, "r", encoding="utf-8") as f:
		full_text = f.read()
		print("markdownの読み込みに成功")	

	# mdファイルを翻訳する前に、obsidian用にパスの書き換え
	with open(input_path, "w", encoding="utf-8") as out:
		out.write(remove_figures_prefix(full_text))

	paragraphs = split_paragraphs(full_text)
	
	print("=== 翻訳処理開始 ===")
		
	with open(output_path, "w", encoding="utf-8") as out:
		for i, paragraph in enumerate(paragraphs, start=1):
			translated = text2jp(paragraph)
			print(f"Wrote: paragraph{i}", flush=True)
			out.write(translated + "\n\n")

	print(f"=== 翻訳完了 {output_path} に保存しました ===", flush=True)
	estimated_fee(get_token(full_text))
	input("終了するにはEnterキーを押してください")

if __name__ == "__main__":
	main()
