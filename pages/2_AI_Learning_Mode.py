import streamlit as st

# --- Custom CSS (Replicated for consistency across all pages) ---
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
        padding: 12px 25px; /* Larger buttons */
        border-radius: 10px; /* More rounded buttons */
        border: none;
        cursor: pointer;
        font-size: 18px; /* Larger font */
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
        box_shadow: inset 0 1px 3px rgba(0,0,0,0.05);
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
        font-size: 22px;
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
        font-size: 24px;
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
        font-size: 24px;
    }

    .stAlert {
        border-radius: 10px;
    }
    .stImage {
        border-radius: 15px;
        overflow: hidden;
    }
    /* New styles for code explanation text */
    .code-explanation {
        background-color: #f0f8ff; /* Light blue background */
        border-left: 5px solid var(--primary-blue);
        padding: 15px;
        margin: 15px 0;
        border-radius: 8px;
        font-size: 24px;
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

# --- Check API Key and Redirect if Missing ---
if "openai_api_key" not in st.session_state or not st.session_state.openai_api_key:
    st.warning("🚨 API Key not found! Please go back to the Home page to set it.")
    if st.button("⬅️ Go to Home Page"):
        st.switch_page("app.py")
    st.stop() # Stop execution if API key is missing

# --- Page Content ---
st.title("🌟 EduSpark: AI Learning Mode! 🌟")
st.markdown("---")

# Display grade selection if not already chosen (this state will reset each time page is loaded)
st.subheader("Choose Your Grade! 🚀")
st.markdown("""
<div class="lesson-card" style="text-align: center;">
    <p>Select your grade to explore amazing AI concepts!</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Grade 3 ✨", key="grade3_select_btn"):
        st.switch_page("pages/Grade_3_chatbot.py")
with col2:
    if st.button("Grade 4 🤖", key="grade4_select_btn"):
        st.switch_page("pages/Grade_4_chatbot.py")
with col3:
    if st.button("Grade 5 💡", key="grade5_select_btn"):
        st.switch_page("pages/Grade_5_chatbot.py")
with col4:
    if st.button("Grade 6 🚀", key="grade6_select_btn"):
        st.switch_page("pages/Grade_6_chatbot.py")

st.markdown("---")
# --- Navigation ---
if st.button("⬅️ Back to Home Page", key="back_to_home_from_ai_hub"):
    st.switch_page("app.py")

# --- Sidebar Footer (always visible) ---
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ for the students of Pakistan! 🇵�")
