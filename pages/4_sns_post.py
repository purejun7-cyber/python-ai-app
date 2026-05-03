import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate

st.set_page_config(page_title="SNS投稿文作成", page_icon="📱", layout="centered")
st.title("📱 SNS 投稿文作成")
st.markdown("各 SNS に最適化した投稿文を自動生成します。")
st.markdown("---")

topic = st.text_area("投稿したい内容・伝えたいこと", height=120, max_chars=500, placeholder="例：新しいカフェに行ってきました。内装がおしゃれで、コーヒーがとても美味しかったです。")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("プラットフォーム", ["Twitter / X（140文字以内）", "Instagram", "LinkedIn（ビジネス向け）", "Facebook", "Threads"])
with col2:
    tone = st.selectbox("トーン", ["フレンドリー・カジュアル", "プロフェッショナル", "エモーショナル・共感", "ユーモア・面白い", "インフォメーション・情報提供"])

use_hashtag = st.checkbox("ハッシュタグを含める", value=True)
use_emoji = st.checkbox("絵文字を含める", value=True)

if st.button("投稿文を生成する", type="primary", use_container_width=True):
    if not topic:
        st.warning("投稿したい内容を入力してください。")
    else:
        with st.spinner("投稿文を生成中..."):
            platform_instructions = {
                "Twitter / X（140文字以内）": "Twitter/X向けに140文字以内で作成してください。",
                "Instagram": "Instagram向けに、視覚的な表現を使い適度な長さで作成してください。",
                "LinkedIn（ビジネス向け）": "LinkedIn向けにプロフェッショナルな内容で、価値提供を意識した投稿を作成してください。",
                "Facebook": "Facebook向けに読みやすい長さで作成してください。",
                "Threads": "Threads向けにカジュアルで読みやすい投稿を作成してください。",
            }
            prompt = f"""以下の内容を元に SNS 投稿文を日本語で作成してください。

【投稿内容】
{topic}

【プラットフォーム指示】: {platform_instructions[platform]}
【トーン】: {tone}
{"ハッシュタグを適切に含めてください。" if use_hashtag else "ハッシュタグは不要です。"}
{"絵文字を適切に使ってください。" if use_emoji else "絵文字は使わないでください。"}

投稿文のみを出力してください（説明文は不要です）。"""
            try:
                result = generate(prompt)
                st.markdown("### 生成された投稿文")
                st.text_area("投稿文（コピーしてご利用ください）", value=result, height=200)
                st.caption(f"文字数: {len(result)} 文字")
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("AIの呼び出しに失敗しました。しばらく待ってから再試行してください。")
