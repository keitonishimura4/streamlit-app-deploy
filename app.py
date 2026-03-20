from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

EXPERT_SYSTEM_MESSAGES = {
    "学習アドバイザー": (
        "あなたは学習アドバイザーです。"
        "相手は初心者だと考え、やさしい日本語で順序立てて説明してください。"
        "専門用語を使うときは短く補足し、最後に次の一歩を1つ提案してください。"
    ),
    "旅行プランナー": (
        "あなたは旅行プランナーです。"
        "相手の希望をくみ取り、現実的でわかりやすい提案を日本語で行ってください。"
        "日程、費用感、持ち物の観点も必要に応じて含めてください。"
    ),
}


def get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    try:
        secret_api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        secret_api_key = None

    if secret_api_key:
        return secret_api_key

    raise ValueError(
        "OPENAI_API_KEY が設定されていません。.env または Streamlit Community Cloud の Secrets に設定してください。"
    )


def normalize_response_content(content: object) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        texts = [normalize_response_content(item) for item in content]
        return "\n".join(text for text in texts if text).strip()

    if isinstance(content, dict):
        texts: list[str] = []
        for key in ("text", "content", "value"):
            value = content.get(key)
            normalized_value = normalize_response_content(value)
            if normalized_value:
                texts.append(normalized_value)
        if texts:
            return "\n".join(texts).strip()

    if content is None:
        return ""

    return str(content).strip()


def get_llm_response(input_text: str, expert_type: str) -> str:
    user_text = input_text.strip()
    if not user_text:
        raise ValueError("入力テキストを入力してください。")

    system_message = EXPERT_SYSTEM_MESSAGES.get(expert_type)
    if system_message is None:
        raise ValueError("専門家の選択が不正です。")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{user_input}"),
        ]
    )

    llm = ChatOpenAI(
        model=DEFAULT_MODEL,
        temperature=0.3,
        api_key=get_api_key(),
    )

    chain = prompt | llm
    response = chain.invoke({"user_input": user_text})
    return normalize_response_content(response.content)


def main() -> None:
    st.set_page_config(page_title="専門家に相談できるLLMアプリ")

    st.title("専門家に相談できるLLMアプリ")
    st.write(
        "このアプリは、入力したテキストを LangChain 経由で LLM に渡し、"
        "選んだ専門家の立場で回答を返す Streamlit アプリです。"
    )
    st.write("操作方法: 1. 専門家を選ぶ 2. 入力欄に相談内容を書く 3. 送信ボタンを押す")

    expert_type = st.radio(
        "専門家の種類を選んでください",
        options=list(EXPERT_SYSTEM_MESSAGES.keys()),
    )

    with st.form("llm_form"):
        input_text = st.text_area(
            "入力テキスト",
            height=180,
            placeholder="例: Pythonの勉強を1週間で始める計画を作ってください。",
        )
        submitted = st.form_submit_button("送信")

    if not submitted:
        return

    if not input_text.strip():
        st.warning("入力テキストを入力してください。")
        return

    try:
        with st.spinner("LLM が回答を作成しています..."):
            answer = get_llm_response(input_text, expert_type)
        st.subheader("回答結果")
        st.markdown(answer)
    except Exception as error:
        st.error(f"エラーが発生しました: {error}")


if __name__ == "__main__":
    main()
