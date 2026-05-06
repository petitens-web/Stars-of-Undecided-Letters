import streamlit as st
from datetime import datetime
import uuid

# 1. Page Configuration
st.set_page_config(page_title="Stars of Undecided Letters", page_icon="✨", layout="centered")

# 2. Ultra-Aesthetic Midnight CSS
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
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 200;
        letter-spacing: 1px;
        color: #9ca3af !important;
        background-color: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #fbbf24 !important;
        border-bottom: 1px solid #fbbf24 !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #fbbf24 !important;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.2) !important;
    }

    /* Star Button - The "Caly" Vibe */
    div.stButton > button {
        background: transparent;
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 50% !important;
        width: 70px;
        height: 70px;
        font-size: 28px;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 10px auto;
        display: block;
    }
    div.stButton > button:hover {
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid #fbbf24;
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
        transform: scale(1.1) rotate(15deg);
    }

    /* Revealed Letter Card */
    .letter-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(251, 191, 36, 0.1);
        padding: 40px;
        border-radius: 24px;
        margin-top: 25px;
        animation: slideUp 1s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .letter-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 24px;
        line-height: 1.6;
        color: #f3f4f6;
        font-style: italic;
        text-align: center;
    }

    .letter-meta {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        color: #fbbf24;
        margin-top: 30px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 10px;
        color: #374151;
        margin-top: 100px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State Initialization
if 'letters_db' not in st.session_state:
    st.session_state.letters_db = []

# --- HEADER ---
st.markdown('<p class="pety-brand">PETY</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Stars of Undecided Letters</h1>', unsafe_allow_html=True)

# --- MAIN NAVIGATION ---
tab1, tab2 = st.tabs(["🔍 Search the Sky", "✍️ Write a Letter"])

with tab1:
    st.write("<br>", unsafe_allow_html=True)
    search_name = st.text_input("", placeholder="Enter your name...", key="search_input")
    
    if search_name:
        query = search_name.lower().strip()
        results = [l for l in st.session_state.letters_db if l['to'] == query]
        
        if results:
            st.markdown(f"<p style='text-align:center; color:#fbbf24;'>✨ Found {len(results)} star(s) for you.</p>", unsafe_allow_html=True)
            
            # Show a glowing star for each result
            for i, res in enumerate(results):
                if st.button("⭐", key=f"star_{i}"):
                    st.session_state[f"reveal_{i}"] = True
                
                if st.session_state.get(f"reveal_{i}", False):
                    st.markdown(f"""
                        <div class="letter-card">
                            <div class="letter-text">"{res['content']}"</div>
                            <div class="letter-meta">FOR: {res['to']} — {res['date']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Let it fade into the void", key=f"fade_{i}"):
                        st.session_state[f"reveal_{i}"] = False
                        st.rerun()
        else:
            st.markdown("<p style='text-align:center; opacity:0.5;'>The sky is quiet for this name... for now.</p>", unsafe_allow_html=True)

with tab2:
    st.write("<br>", unsafe_allow_html=True)
    with st.form("letter_form", clear_on_submit=True):
        to_name = st.text_input("Who is this letter for?", placeholder="Recipient's Name")
        message = st.text_area("Your undecided words...", placeholder="Write the things you never said...", height=150)
        
        submitted = st.form_submit_button("Release to the Stars")
        
        if submitted:
            if to_name and message:
                uid = str(uuid.uuid4())[:8]
                st.session_state.letters_db.append({
                    "id": uid,
                    "to": to_name.lower().strip(),
                    "content": message,
                    "date": datetime.now().strftime("%B %d, %Y").upper()
                })
                st.success("Your words have become a star in the sky.")
                
                # Link generation (Shareable)
                link = f"https://stars-of-undecided-letters.streamlit.app/?id={uid}"
                st.markdown("### 🔗 Share this Secret Star:")
                st.code(link)
            else:
                st.error("Please fill in both fields.")

# --- FOOTER ---
st.markdown('<div class="footer">STARS OF UNDECIDED LETTERS • 2026</div>', unsafe_allow_html=True)