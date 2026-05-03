import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="centered")
st.title("🌐 翻訳")
st.markdown("自然で読みやすい翻訳を生成します。")
st.markdown("---")

text = st.text_area("翻訳したいテキスト", height=200, max_chars=3000, placeholder="ここに翻訳したいテキストを入力してください...")

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("翻訳元の言語", ["自動検出", "日本語", "英語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"])
with col2:
    target_lang = st.selectbox("翻訳先の言語", ["英語", "日本語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"])

style = st.selectbox("翻訳スタイル", ["自然な翻訳（推奨）", "直訳（原文に忠実）", "フォーマル・ビジネス向け", "カジュアル・口語"])

if st.button("翻訳する", type="primary", use_container_width=True):
    if not text:
        st.warning("翻訳したいテキストを入力してください。")
    elif source_lang != "自動検出" and source_lang == target_lang:
        st.warning("翻訳元と翻訳先の言語が同じです。")
    else:
        with st.spinner("翻訳中..."):
            source_instruction = "（言語を自動検出してください）" if source_lang == "自動検出" else f"翻訳元: {source_lang}"
            prompt = f"""以下のテキストを翻訳してください。

【テキスト】
{text}

{source_instruction}
翻訳先: {target_lang}
翻訳スタイル: {style}

翻訳結果のみを出力してください（説明文は不要です）。"""
            try:
                result = generate(prompt)
                st.markdown("### 翻訳結果")
                st.text_area("翻訳結果（コピーしてご利用ください）", value=result, height=200)
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
