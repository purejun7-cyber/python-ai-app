import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="ブログ記事執筆", page_icon="📝", layout="centered")
st.title("📝 ブログ記事執筆")
st.markdown("トピックや条件を指定してブログ記事を自動生成します。")
st.markdown("---")

topic = st.text_input("記事のトピック・テーマ", placeholder="例：初心者向け Python 入門", max_chars=200)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("文体・トーン", ["丁寧・フォーマル", "カジュアル・フレンドリー", "専門的・技術的", "エンタメ・ユーモラス"])
with col2:
    length = st.selectbox("記事の長さ", ["短め（500文字程度）", "普通（1000文字程度）", "長め（2000文字程度）"])

target = st.text_input("ターゲット読者（任意）", placeholder="例：プログラミング初心者、20代会社員", max_chars=100)
keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例：Python, 入門, プログラミング", max_chars=200)

if st.button("記事を生成する", type="primary", use_container_width=True):
    if not topic:
        st.warning("トピックを入力してください。")
    else:
        with st.spinner("記事を生成中..."):
            length_map = {
                "短め（500文字程度）": "500文字程度",
                "普通（1000文字程度）": "1000文字程度",
                "長め（2000文字程度）": "2000文字程度",
            }
            prompt = f"""以下の条件でSEOに強いブログ記事を日本語で書いてください。

トピック: {topic}
文体・トーン: {tone}
記事の長さ: {length_map[length]}
{"ターゲット読者: " + target if target else ""}
{"含めるキーワード: " + keywords if keywords else ""}

【出力形式】
以下の構成で必ず出力してください。

## メタディスクリプション
（100〜120文字で記事の内容を要約。検索結果のスニペットとして使える文章）

## 記事本文

# （キーワードを含むSEOタイトル）

**この記事のポイント（冒頭まとめ）**
- 記事で得られる情報を箇条書きで3〜5点

（本文）
- 見出しはH2・H3を使って階層構造にする
- 指定キーワードを不自然にならない範囲で見出しと本文に散りばめる
- 結論や要点は冒頭にも記載し、読者がすぐ価値を得られるようにする

## 関連トピック（内部リンク候補）
（この記事と関連性が高く、内部リンクとして繋げると効果的なトピックを3〜5個提案）

Markdown 形式で出力してください。"""
            try:
                result = generate(prompt)
                st.markdown("### 生成された記事")
                st.markdown(result)
                st.download_button(
                    label="テキストとしてダウンロード",
                    data=result,
                    file_name="blog_article.md",
                    mime="text/markdown",
                )
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
