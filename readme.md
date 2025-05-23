# translate.py

## このスクリプトについて
本スクリプトは、研究室内での論文読解効率化を目的に作成したツールです。  
PDF論文をOCRでMarkdownに変換し、OpenAI APIを用いて日本語に意訳します。  
出力は Obsidian にそのまま読み込める形式に整えられています。
プロンプトや全体の流れ、ライブラリなど多大に以下の記事を参考にしています：

- [Notionに論文を登録すると数式もふくめよしなに翻訳してくれるフローを構築した](https://qiita.com/tsukemono/items/9b466e94e4467d3a6f2b)

ただし、本スクリプトでは自分および研究室内の用途に合わせた独自のアレンジを加えています。

## アレンジ点

- トークナイザを利用し、API料金の自動見積もり機能をつけた
- Markdown内の画像リンクを Obsidian 用に自動修正
- md,txtなど、pdf以外の入力も受けつけ、翻訳のみの利用もできるようにした

## 仕様
初回はコマンドプロンプトで

<pre><code>$ pip install openai tiktoken pix2text</code></pre>
を実行してください。
14行めにAPIKeyを書く場所があるので、そこにAPIKeyを入力してください。
コマンドプロンプト上でtranslate.pyがあるフォルダに移動し、以下のように入力すれば実行できます。
<pre><code>$ python translate.py 入力したいファイル 出力してほしい名前.md</code></pre>