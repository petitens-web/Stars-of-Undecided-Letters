import streamlit as st
from datetime import datetime
import uuid

# 1. Page Configuration
st.set_page_config(page_title="Stars of Undecided Letters", page_icon="✨", layout="centered")

# 2. Updated Aesthetic CSS (Fixed Input Font Color)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,400&family=Inter:wght@200;400&display=swap');

    /* Global Background */
    .stApp {
        background: radial-gradient(circle at top, #0d1117 0%, #000000 100%);
        color: #e5e7eb;
    }

    /* Branding Header */
    .pety-brand {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        letter-spacing: 6px;
        text-align: center;
        color: #fbbf24;
        opacity: 0.6;
        text-transform: uppercase;
        margin-bottom: -15px;
    }

    /* Main Title */
    .main-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        text-align: center;
        background: linear-gradient(to bottom, #ffffff 30%, #4b5563 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-style: italic;
        margin-bottom: 30px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 200;
        color: #9ca3af !important;
    }
    .stTabs [aria-selected="true"] {
        color: #fbbf24 !important;
        border-bottom: 1px solid #fbbf24 !important;
    }

    /* --- FIXED INPUT FONT COLOR --- */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #f3f4f6 !important; /* Light gray background */
        color: #000000 !important;             /* BLACK FONT COLOR */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif;
    }

    /* Star Button */
    div.stButton > button {
        background: transparent;
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 50% !important;
        width: 70px;
        height: 70px;
        font-size: 28px;
        transition: all 0.5s ease;
        margin: 10px auto;
        display: block;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
        transform: scale(1.1);
    }

    /* Revealed Letter Card */
    .letter-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(251, 191, 36, 0.1);
        padding: 40px;
        border-radius: 24px;
        margin-top: 25px;
    }

    .letter-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        line-height: 1.6;
        color: #f3f4f6;
        font-style: italic;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

if 'letters_db' not in st.session_state:
    st.session_state.letters_db = []

# --- UI CONTENT ---
st.markdown('<p class="pety-brand">PETY</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Stars of Undecided Letters</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Search the Sky", "✍️ Write a Letter"])

with tab1:
    search_name = st.text_input("", placeholder="Enter your name to search...", key="search")
    if search_name:
        query = search_name.lower().strip()
        results = [l for l in st.session_state.letters_db if l['to'] == query]
        if results:
            for i, res in enumerate(results):
                if st.button("⭐", key=f"star_{i}"):
                    st.markdown(f'<div class="letter-card"><div class="letter-text">"{res["content"]}"</div></div>', unsafe_allow_html=True)
        else:
            st.info("The sky is quiet for this name.")

with tab2:
    with st.form("letter_form", clear_on_submit=True):
        to_name = st.text_input("Who is this letter for?", placeholder="Recipient's Name")
        message = st.text_area("Your undecided words...", placeholder="Write the things you never said...")
        if st.form_submit_button("Release to the Stars"):
            if to_name and message:
                st.session_state.letters_db.append({
                    "to": to_name.lower().strip(),
                    "content": message,
                    "date": datetime.now().strftime("%B %d, %Y")
                })
                st.success("Your words have become a star.")