
import streamlit as st
from groq import Groq, RateLimitError, APIError


def get_hosted_answer(messages):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        return "Hosted AI isn't configured yet."

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
        )

        return response.choices[0].message.content or "No answer generated."

    except RateLimitError:
        return (
            "⏳ **AI is temporarily busy.** "
            "You've reached the free AI usage limit. "
            "Please try again later.\n\n"
            "Your uploaded PDFs are still available."
        )

    except APIError as error:
        print(f"Groq API error: {type(error).__name__}")
        return "The AI service is unavailable. Please try again later."
