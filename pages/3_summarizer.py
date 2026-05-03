import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="文章要約", page_icon="📄", layout="centered")
st.title("📄 文章要約")
st.markdown("長い文章を短くまとめます。")
st.markdown("---")

text = st.text_area("要約したい文章", height=300, max_chars=10000, placeholder="ここに要約したい文章を貼り付けてください...")

col1, col2 = st.columns(2)
with col1:
    length = st.selectbox("要約の長さ", ["1〜2文（超短縮）", "3〜5文（短め）", "100〜150文字", "200〜300文字", "箇条書き3点", "箇条書き5点"])
with col2:
    style = st.selectbox("要約スタイル", ["重要ポイントを抽出", "全体の流れを保持", "結論を中心に", "初心者にわかりやすく"])

if st.button("要約する", type="primary", use_container_width=True):
    if not text:
        st.warning("要約したい文章を入力してください。")
    else:
        with st.spinner("要約中..."):
            prompt = f"""以下の文章を日本語で要約してください。

【文章】
{text}

【要約の長さ】: {length}
【要約スタイル】: {style}

指定された長さとスタイルに従って要約してください。"""
            try:
                result = generate(prompt)
                st.markdown("### 要約結果")
                st.info(result)

                original_len = len(text)
                summary_len = len(result)
                ratio = round((1 - summary_len / original_len) * 100) if original_len > 0 else 0
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("元の文字数", f"{original_len} 文字")
                col_b.metric("要約後の文字数", f"{summary_len} 文字")
                col_c.metric("圧縮率", f"{ratio}%")
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
