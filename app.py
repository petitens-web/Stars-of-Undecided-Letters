import streamlit as st
from datetime import datetime
import uuid # For generating unique message IDs

# 1. Page Configuration & Custom Styling
st.set_page_config(page_title="Stars of Undecided Letters", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* Midnight sky gradient background */
    .stApp { 
        background: radial-gradient(circle at center, #0b0d17 0%, #050505 100%); 
        color: #e0e0e0; 
    }
    /* Title styling with typewriter effect */
    .main-title { 
        font-family: 'Courier New', monospace; 
        font-size: 35px; 
        text-align: center; 
        color: #ffffff; 
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    /* Glowing star button styling */
    .stButton>button { 
        background: transparent; 
        color: #FFD700; 
        border: 1px solid #FFD700; 
        border-radius: 50%; 
        width: 60px; 
        height: 60px; 
        font-size: 25px; 
        transition: 0.3s;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 20px #FFD700; 
        background: #FFD700; 
        color: #000; 
    }
    /* Aesthetic letter box for revealed messages */
    .letter-box { 
        background: rgba(255,255,255,0.05); 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid rgba(255,215,0,0.3); 
        backdrop-filter: blur(10px); 
        animation: fadeIn 1.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Database & URL Logic
if 'undecided_letters' not in st.session_state:
    st.session_state.undecided_letters = []

# Handling Direct Links via ID (e.g., your-app.com/?id=8charid)
query_params = st.query_params
msg_id = query_params.get("id", "")

st.markdown('<h1 class="main-title">Stars of Undecided Letters</h1>', unsafe_allow_html=True)

# --- DIRECT LINK VIEW ---
if msg_id:
    # Search for the specific letter using the unique ID
    found_letter = next((m for m in st.session_state.undecided_letters if m['id'] == msg_id), None)
    
    if found_letter:
        st.write("<p style='text-align: center;'>A star has been shared with you...</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("⭐", key="direct_star"):
                st.session_state.show_direct = True
        
        if st.session_state.get("show_direct", False):
            st.markdown(f"""
            <div class="letter-box">
                <small style='color:#888;'>POSTMARKED: {found_letter['time']}</small>
                <p style='font-size:20px; font-family:Courier New; margin-top:10px;'>{found_letter['content']}</p>
                <p style='text-align:right; color:#FFD700;'>— For: {found_letter['to'].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Close Letter"):
                st.session_state.show_direct = False
                st.rerun()
    else:
        st.error("This star has already faded or the link is incorrect.")
    
    st.markdown("---")
    if st.button("Write your own undecided letter"):
        st.query_params.clear()
        st.rerun()

# --- MAIN NAVIGATION ---
else:
    tab1, tab2 = st.tabs(["🔍 Search the Sky", "✍️ Write a Letter"])

    # Tab 1: General Search (Like SendTheSong)
    with tab1:
        st.write("Enter your name to see if any stars are shining for you.")
        search_query = st.text_input("Receiver's Name", placeholder="Enter your name...")
        
        if search_query:
            query = search_query.lower().strip()
            results = [m for m in st.session_state.undecided_letters if m['to'] == query]
            
            if results:
                st.write(f"✨ Found {len(results)} star(s) for you. Click to reveal:")
                cols = st.columns(5)
                for i, res in enumerate(results):
                    with cols[i % 5]:
                        if st.button("⭐", key=f"s_{i}"):
                            st.info(f"Message: {res['content']}")
            else:
                st.info("The sky is quiet for this name... for now.")

    # Tab 2: Send Message & Generate Link
    with tab2:
        with st.form("letter_form", clear_on_submit=True):
            to_name = st.text_input("Who is this letter for?", placeholder="Recipient's Name")
            message = st.text_area("Your undecided words...", placeholder="Write the things you never said...")
            
            if st.form_submit_button("Release to the Stars"):
                if to_name and message:
                    unique_id = str(uuid.uuid4())[:8] # Short 8-character unique ID
                    st.session_state.undecided_letters.append({
                        "id": unique_id,
                        "to": to_name.lower().strip(),
                        "content": message,
                        "time": datetime.now().strftime("%d %b %Y").upper()
                    })
                    st.success("Your words have become a star in the sky.")
                    
                    # LINK GENERATION 
                    # Replace the URL below with your actual Streamlit URL after deployment
                    current_url = "https://stars-of-undecided-letters.streamlit.app/" 
                    temp_link = f"{current_url}?id={unique_id}"
                    
                    st.markdown("### 🔗 Share this Secret Star:")
                    st.code(temp_link) # Creates a copyable link box
                    st.write("Send this temporary link to them. Only someone with this link can view this specific star.")
                else:
                    st.error("Every star needs a destination and a story. Please fill in both fields.")

st.markdown("<br><hr style='opacity:0.2;'>", unsafe_allow_html=True)
st.caption("Stars of Undecided Letters © 2026")