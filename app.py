import streamlit as st
import re

from src.ingestion.youtube_loader import load_video
from src.processing.chunking import split_docs
from src.rag.pipeline import build_index, ask
from src.agents.tutor_agent import generate_questions

st.title("🎥 AI YouTube Assistant")

# 🔥 Extract video ID from input (ID or URL)
def extract_video_id(input_value):
    input_value = input_value.strip()

    # Case 1: Already a YouTube URL
    if "youtube.com" in input_value or "youtu.be" in input_value:
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", input_value)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")

    # Case 2: Raw ID
    if len(input_value) == 11:
        return input_value

    raise ValueError("Invalid YouTube Video ID")

# 🔥 Convert ID → proper URL
def build_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


# Input field
user_input = st.text_input("Enter YouTube Video ID or URL").strip()

if st.button("Process Video"):
    try:
        video_id = extract_video_id(user_input)   # 🔥 smart extraction
        url = build_url(video_id)                 # 🔥 always valid format

        docs = load_video(url)
        chunks = split_docs(docs)
        build_index(chunks)

        st.success("✅ Video processed successfully!")
        st.info(f"🎬 Video ID: {video_id}")

    except Exception as e:
        st.error(f"❌ Error: {e}")


query = st.text_input("Ask your question")

if query:
    try:
        st.write(ask(query))
    except Exception as e:
        st.error(f"❌ Error: {e}")


if st.button("Generate Questions"):
    try:
        st.write(generate_questions("lecture content"))
    except Exception as e:
        st.error(f"❌ Error: {e}")