import streamlit as st
import json
from yt_dlp import YoutubeDL
from groq import Groq

# Mobile-friendly title
st.title("🎬 AI Video Clipper")
st.caption("Extract viral hooks from YouTube links on your phone.")

# Inputs
api_key = st.text_input("Your Free Groq API Key", type="password", placeholder="gsk_...")
youtube_url = st.text_input("YouTube Video Link", placeholder="https://youtube.com...")

if st.button("🚀 Generate Viral Clips", type="primary"):
    if not youtube_url or not api_key:
        st.error("Please fill in both fields.")
    else:
        with st.spinner("AI is analyzing the video..."):
            try:
                client = Groq(api_key=api_key)
                
                ydl_opts = {'writeautomaticsub': True, 'subtitlesformat': 'json3', 'skip_download': True}
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=False)
                    video_title = info.get('title', 'Video')
                
                system_prompt = "You are an expert AI video editor. Return data strictly in clean JSON format."
                user_prompt = f"Analyze '{video_title}'. Identify 3 viral hooks (30-60s). Return JSON with keys: start_time, end_time, clip_title, viral_reason."

                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"}
                )
                
                ai_data = json.loads(completion.choices.message.content)
                st.json(ai_data)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
