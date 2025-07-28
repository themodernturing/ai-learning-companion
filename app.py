import streamlit as st
import os
from dotenv import load_dotenv # For loading environment variables locally

# --- Load Environment Variables (for local development) ---
load_dotenv()

# --- Configuration ---
st.set_page_config(
    page_title="EduSpark Pakistan: Your AI Learning Companion",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed" # Start collapsed for a clean home page
)

# --- Custom CSS (Centralized for consistency, replicated in other pages) ---
st.markdown("""
    <style>
    :root {
        --primary-blue: #1a73e8; /* A vibrant blue */
        --light-blue-bg: #e8f0fe; /* Very light blue for main background */
        --card-bg: #ffffff; /* White for cards */
        --text-color: #3c4043; /* Dark gray for text */
        --heading-color: #174ea6; /* Darker blue for headings */
        --user-chat-bubble: #e0f7fa; /* Light cyan for user chat */
        --bot-chat-bubble: #f0f8ff; /* Alice blue for bot chat */
    }

    .main {
        background-color: var(--light-blue-bg);
        padding: 20px;
        border-radius: 15px; /* More rounded corners */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); /* Stronger shadow */
    }
    .stButton>button {
        background-color: var(--primary-blue);
        color: white;
        padding: 15px 30px; /* Larger buttons for main navigation */
        border-radius: 12px; /* More rounded buttons */
        border: none;
        cursor: pointer;
        font-size: 20px; /* Larger font */
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 10px; /* Space between buttons */
    }
    .stButton>button:hover {
        background-color: #174ea6; /* Slightly darker blue on hover */
        transform: translateY(-2px); /* Slight lift effect */
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #a0c3f7; /* Blue border */
        padding: 12px;
        font-size: 16px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: var(--heading-color);
        text-align: center;
        font-weight: 800; /* Extra bold */
        margin-bottom: 20px;
    }
    .lesson-card {
        background-color: var(--card-bg);
        border-radius: 15px;
        padding: 25px; /* More padding */
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        color: var(--text-color);
        font-size: 22px; /* Increased font size for readability */
        line-height: 1.6;
    }
    /* Styling for interactive chatbot answers */
    .chat-message-bot {
        background-color: #FFFF00; /* Pure bright yellow for bot chat - EXTREMELY HIGHLY VISIBLE */
        border-radius: 25px; /* More rounded */
        padding: 35px; /* Even more padding */
        margin-bottom: 35px; /* More space below */
        text-align: left;
        margin-right: 5%; /* Make it almost full width */
        box-shadow: -8px 8px 25px rgba(0,0,0,0.7); /* Much stronger shadow */
        color: black; /* Black text for maximum contrast on bright yellow */
        font-size: 42px; /* Significantly larger font for bot answers */
        font-weight: bold; /* Make text bold */
    }
    /* Styling for user messages in interactive chatbots */
    .chat-message-user {
        background-color: var(--user-chat-bubble);
        border-radius: 20px; /* Even more rounded */
        padding: 15px;
        margin-bottom: 12px;
        text-align: right;
        margin-left: 25%; /* Wider bubbles */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.15);
        color: var(--text-color);
        font-size: 22px; /* Consistent with lesson-card text */
    }

    /* Specific styling for the "Seeing is Believing" simulated chat */
    .simulated-chat-message-user {
        background-color: #e0f7fa; /* Light cyan */
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: right;
        margin-left: 25%;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.15);
        color: var(--text-color);
        font-size: 24px; /* Appropriate size for simulated chat */
    }
    .simulated-chat-message-bot {
        background-color: #f0f8ff; /* Alice blue */
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 12px;
        text-align: left;
        margin-right: 25%;
        box-shadow: -2px 2px 5px rgba(0,0,0,0.15);
        color: var(--text-color);
        font-size: 24px; /* Appropriate size for simulated chat */
    }

    .stAlert {
        border-radius: 10px;
    }
    .stImage {
        border-radius: 15px;
        overflow: hidden; /* Ensures image corners are rounded */
    }
    /* New styles for code explanation text */
    .code-explanation {
        background-color: #f0f8ff; /* Light blue background */
        border-left: 5px solid var(--primary-blue);
        padding: 15px;
        margin: 15px 0;
        border-radius: 8px;
        font-size: 24px; /* Larger font for explanations */
        color: var(--text-color);
    }
    /* Custom styles for Wednesday Addams themed section */
    .dark-lesson-card {
        background-color: #1a1a1a; /* Very dark grey/black */
        color: #f0f0f0; /* Light text */
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        font-size: 22px;
        line-height: 1.6;
    }
    .dark-header {
        color: #000000; /* Black for the header text */
        text-align: center;
        font-weight: 800;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- API Key Loading and Session State Management ---
# Attempt to load API key from environment variables (for local .env file)
openai_api_key = os.getenv("OPENAI_API_KEY")

# If not found in environment variables, try Streamlit secrets (for Streamlit Cloud deployment)
if not openai_api_key:
    openai_api_key = st.secrets.get("OPENAI_API_KEY")

# Store the API key in session state for access across all pages
if openai_api_key:
    st.session_state.openai_api_key = openai_api_key
    st.session_state.api_key_loaded = True
else:
    st.session_state.api_key_loaded = False
    st.session_state.openai_api_key = None # Ensure it's explicitly None if not found

# --- Main Home Page Content ---
st.title("🌟 Welcome to EduSpark Pakistan! 🌟")
st.markdown("---")

st.markdown("""
<div class="lesson-card" style="text-align: center;">
    <p>Your ultimate companion for learning about AI and asking questions!</p>
    <p>Choose your adventure below:</p>
</div>
""", unsafe_allow_html=True)

# Display a warning if API key is not loaded
if not st.session_state.api_key_loaded:
    st.warning("""
        🚨 **API Key Missing!** 🚨
        To use the chatbot features, please set your `OPENAI_API_KEY` environmental variable.
        
        **For Local Development:** Create a `.env` file in your project's root directory with `OPENAI_API_KEY="your_key_here"`.
        **For Streamlit Cloud:** Go to your app's settings -> 'Secrets' and add `OPENAI_API_KEY`.
        
        You can still explore the app's structure, but interactive AI features will not work.
    """)
    # Disable buttons if API key is not loaded
    disable_buttons = True
else:
    disable_buttons = False

# Main navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("💬 Go to Q&A Chatbot", key="go_to_qa_chatbot_btn", disabled=disable_buttons):
        st.switch_page("pages/1_Student_Mode.py") # Navigate to your Q&A chatbot page

with col2:
    if st.button("🤖 Enter AI Learning Mode", key="go_to_ai_learning_btn", disabled=disable_buttons):
        st.switch_page("pages/2_AI_Learning_Mode.py") # Navigate to the AI Learning Hub

st.markdown("---")
st.info("Developed with ❤️ for the students of Pakistan! 🇵�")
