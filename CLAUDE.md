# [CLAUDE.md](http://CLAUDE.md)

このファイルは、このリポジトリでコードを扱うときの Claude Code（claude.ai/code）向けのガイドです。

## コマンド

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py

# 環境のセットアップ
cp .env.example .env  # 続けて .env に GEMINI_API_KEY を設定
```

テストスイートやリンターは設定されていません。

## アーキテクチャ

日本語向けの **Streamlit マルチページの AI ライティングアシスタント**で、Google Gemini 2.0 Flash を利用しています。

**データの流れ:** 各ページがユーザー入力からプロンプトを組み立て → `utils/gemini_client.generate(prompt)` を呼び出し → 結果を表示します。

`**utils/gemini_client.py`** が共有の唯一のモジュールです。`.env` から `GEMINI_API_KEY` を読み込み、Gemini モデルを初期化し、関数 `generate(prompt: str) -> str` を 1 つ公開しています。各ページは `sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` 経由でこれをインポートします。

**ページ**（`pages/`）はサイドバーの並びを制御するため番号付きです。それぞれ `st.set_page_config()`、入力ウィジェット、プロンプト組み立て、出力表示が自己完結しており、ページ間で共有状態はありません。

## 新しいページを追加するとき

全ページが共通のボイラープレートを持つ。新規ページはこれをベースにする：

```python
import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="ページ名", page_icon="🔤", layout="centered")
st.title("🔤 ページ名")
st.markdown("---")

# 入力ウィジェット

if st.button("実行", type="primary", use_container_width=True):
    if not user_input:
        st.warning("入力してください。")
    else:
        with st.spinner("生成中..."):
            try:
                result = generate(prompt)
                st.markdown(result)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
```

ファイル名の番号（`N_`）がサイドバーの表示順を決める。

## モデルの変更

使用モデルは `utils/gemini_client.py` の1か所で管理している：

```python
return genai.GenerativeModel("gemini-2.5-flash")  # ここを変更
```

`get_client()` は `generate()` を呼ぶたびに実行されるため（インスタンスのキャッシュなし）、モデルを重いものに変えると全ページの応答速度に影響する。

## プロンプト構築の慣習

- selectbox の値を日本語表示のまま `f-string` に埋め込んでプロンプトを構成する
- 任意入力は `if value` で条件付きで追加する（例: `{"キーワード: " + kw if kw else ""}`）
- 出力形式を明示する（`Markdown 形式で出力`, `翻訳結果のみを出力` など）
- セレクトボックスの表示文字列とプロンプト用文字列が異なる場合は `length_map` のような辞書でマッピングする

