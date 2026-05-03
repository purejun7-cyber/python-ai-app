import streamlit as st

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI ライティングツール")
st.markdown("---")

st.markdown("""
個人用の AI ライティングアシスタントです。サイドバーから使いたい機能を選んでください。

### 機能一覧

| 機能 | 説明 |
|------|------|
| 📝 ブログ記事執筆 | トピックや条件を指定して記事を自動生成 |
| 📧 メール返信 | 受信メールに対する返信文を作成 |
| 📄 文章要約 | 長文を指定した長さに要約 |
| 📱 SNS 投稿文 | Twitter / Instagram 向けの投稿文を作成 |
| 🔍 文章校正・添削 | 文章の誤りや改善点を指摘・修正 |
| 🌐 翻訳 | 日本語 ↔ 英語・中国語・韓国語などに翻訳 |
""")

st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash")
