import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="メール返信", page_icon="📧", layout="centered")
st.title("📧 メール返信")
st.markdown("受信したメールを貼り付けると、返信文を自動作成します。")
st.markdown("---")

original = st.text_area("受信メールの内容", height=200, max_chars=5000, placeholder="ここに受信したメールの本文を貼り付けてください...")

col1, col2 = st.columns(2)
with col1:
    intent = st.selectbox("返信の意図", ["承諾・了解", "丁重に断る", "質問・確認する", "感謝する", "詳細を送る", "日程を調整する"])
with col2:
    tone = st.selectbox("文体", ["ビジネス敬語（丁寧）", "カジュアル", "フォーマル（格式高め）"])

extra = st.text_area("追加で伝えたい内容（任意）", height=80, max_chars=300, placeholder="例：来週の月曜日は都合が悪いです。火曜日以降であれば対応可能です。")

if st.button("返信文を作成する", type="primary", use_container_width=True):
    if not original:
        st.warning("受信メールの内容を入力してください。")
    else:
        with st.spinner("返信文を作成中..."):
            prompt = f"""以下のメールへの返信文を日本語で作成してください。

【受信メール】
{original}

【返信の意図】: {intent}
【文体】: {tone}
{"【追加で伝えたい内容】: " + extra if extra else ""}

件名（Re:〜）と本文（挨拶・本題・締め）を含む完成した返信メールを出力してください。"""
            try:
                result = generate(prompt)
                st.markdown("### 生成された返信文")
                st.text_area("返信文（コピーしてご利用ください）", value=result, height=300)
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
