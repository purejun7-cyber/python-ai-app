import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="文章校正・添削", page_icon="🔍", layout="centered")
st.title("🔍 文章校正・添削")
st.markdown("文章の誤りや改善点を指摘し、修正案を提示します。")
st.markdown("---")

text = st.text_area("校正したい文章", height=250, max_chars=5000, placeholder="ここに校正・添削したい文章を入力してください...")

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("校正モード", ["誤字・脱字チェック", "文法・表現の改善", "敬語・ビジネス文章に整える", "わかりやすく書き直す", "全て（総合校正）"])
with col2:
    output_style = st.selectbox("出力形式", ["修正後の文章 + 修正箇所の説明", "修正箇所の指摘のみ", "修正後の文章のみ"])

if st.button("校正する", type="primary", use_container_width=True):
    if not text:
        st.warning("校正したい文章を入力してください。")
    else:
        with st.spinner("校正中..."):
            prompt = f"""以下の文章を日本語で校正・添削してください。

【文章】
{text}

【校正モード】: {mode}
【出力形式】: {output_style}

指定された校正モードと出力形式に従って結果を出力してください。"""
            try:
                result = generate(prompt)
                st.markdown("### 校正結果")
                st.markdown(result)
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
