
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import streamlit as st
from io import BytesIO

# =============================
# LOAD API & CONFIG
# =============================
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# =============================
# APP UI SETUP
# =============================
st.set_page_config(page_title="AI Image Analyzer Pro", page_icon="🧠", layout="wide")

# Custom CSS styling for dark mode + modern UI
st.markdown(
    """
    <style>
        body {background-color: #0e1117;}
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: white !important;
        }
        .stTextInput > div > div > input {
            background-color: #1e222a;
            color: white;
            border-radius: 8px;
            border: 1px solid #3b82f6;
        }
        .stButton > button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2563eb;
            transform: scale(1.05);
        }
        .stDownloadButton > button {
            background-color: #22c55e;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stDownloadButton > button:hover {
            background-color: #16a34a;
        }
        .stSidebar {
            background-color: #111827;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# APP HEADER
# =============================
st.title("🧠 AI Image Analyzer")
st.caption("Upload an image, ask anything — powered by Gemini ")

# =============================
#  SIDEBAR SETTINGS
# =============================
st.sidebar.header("⚙️ Settings")
model_name = st.sidebar.selectbox("Select Model", ["gemini-2.0-flash"])
creativity = st.sidebar.slider("🎨 Creativity Level (temperature)", 0.0, 1.0, 0.5)
st.sidebar.markdown("---")

# =============================
# FILE UPLOAD
# =============================
uploaded_file = st.file_uploader("📸 Upload an Image", type=["png", "jpg", "jpeg"])

# Session storage for chat-like memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # Prompt input
    prompt = st.text_input("💬 Enter your prompt or question about the image")

    # Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        analyze = st.button("🚀 Analyze Image")
    with col2:
        caption_btn = st.button("🖼️ Generate Caption")
    with col3:
        emotion_btn = st.button("😃 Detect Emotion")

    model = genai.GenerativeModel(model_name)
    response_text = ""

    # =============================
    # RESPONSE HANDLERS
    # =============================
    if analyze and prompt:
        with st.spinner("Analyzing image with your prompt... 🔍"):
            response = model.generate_content([prompt, img], generation_config={"temperature": creativity})
        response_text = response.text
        st.session_state.chat_history.append(("🧠 Prompt", prompt))
        st.session_state.chat_history.append(("💡 Response", response_text))

    elif caption_btn:
        with st.spinner("Generating caption... 🖼️"):
            response = model.generate_content(["Describe this image in one detailed caption.", img])
        response_text = response.text
        st.session_state.chat_history.append(("🖼️ Caption", response_text))

    elif emotion_btn:
        with st.spinner("Detecting emotion... 😃"):
            response = model.generate_content(["What emotion or mood does this image convey?", img])
        response_text = response.text
        st.session_state.chat_history.append(("😃 Emotion", response_text))

    # =============================
    # DOWNLOAD FEATURE
    # =============================
    if response_text:
        st.subheader("✨ Response:")
        st.markdown(f"🪄 **{response_text}**")
        buffer = BytesIO(response_text.encode())
        st.download_button("📥 Download Response", buffer, file_name="response.txt")

# =============================
#  CHAT HISTORY SECTION
# =============================
if st.session_state.chat_history:
    st.sidebar.markdown("## 💬 Chat History")
    for i, (role, msg) in enumerate(reversed(st.session_state.chat_history)):
        st.sidebar.markdown(f"**{role}:** {msg}")
