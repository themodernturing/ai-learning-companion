import streamlit as st
import time # For simulating animations/delays
import os # For checking if image file exists

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
        font-size: 22px; /* Increased font size for readability for 8-year-olds */
        line-height: 1.6;
    }
    /* Styling for the interactive chatbot answers (e.g., Harry Potter) */
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
    /* Styling for the user messages in interactive chatbots */
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
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---

def scroll_to_top():
    """Injects JavaScript to scroll the page to the top."""
    st.markdown(
        """
        <script>
            window.parent.document.querySelector('.main').scrollTop = 0;
        </script>
        """,
        unsafe_allow_html=True
    )

# --- Check API Key and Redirect if Missing ---
# This section ensures the API key is loaded from session_state (set in app.py)
if "openai_api_key" not in st.session_state or not st.session_state.openai_api_key:
    st.warning("🚨 API Key not found! Please go back to the Home page to set it.")
    if st.button("⬅️ Go to Home Page"):
        st.switch_page("app.py")
    st.stop() # Stop execution if API key is missing


# --- Main App Content (displayed after API key is entered) ---
# All content is now on a single page, rendered sequentially.

st.title("🌟 EduSpark: AI & Chatbots for Grade 4! 🌟")
st.markdown("---")


# --- Welcome & What is AI? (Grade 4) ---
st.header("What is AI? 🧠✨")
st.markdown("""
<div class="lesson-card">
    <p>Imagine computers that can **THINK** and **LEARN**! 🤯 That's **AI**!</p>
    <p>It's like teaching a robot to be super smart and helpful. 🤖</p>
    <p>AI helps make cool games, smart toys, and even helps grown-ups with tricky jobs! 🎮🤖</p>
    <p>Learning AI is fun! ✨ And with EduSpark, you're going to **ACE IT!** 🏆</p>
</div>
""", unsafe_allow_html=True)


# --- AI is Everywhere! / Snoopy (Grade 4 specific: Shapes) ---
st.header("AI is Everywhere! Can you spot it? 🕵️‍♀️")
st.markdown("""
<div class="lesson-card">
    <p>Let's meet **Snoopy the Smart Dog!** 🐶💡 Snoopy can learn new tricks and even understand your commands! That's AI magic! ✨</p>
    <p>We'll show you how Snoopy learns to recognize **shapes**! 👇</p>
</div>
""", unsafe_allow_html=True)

# Initialize Snoopy's state for automatic animation
if "snoopy_animation_started_g4" not in st.session_state:
    st.session_state.snoopy_animation_started_g4 = False
if "snoopy_current_message_index_g4" not in st.session_state:
    st.session_state.snoopy_current_message_index_g4 = 0

snoopy_messages_g4 = [
    "You show Snoopy a **SQUARE**! 🟪",
    "Snoopy looks closely at the shape! 👀",
    "Snoopy learns: 'This is a **SQUARE**!' 🧠",
    "Now, you show Snoopy another shape: a **CIRCLE**! 🔵",
    "Snoopy says: 'That's a **CIRCLE**!' 🎉",
]

# Placeholder for Snoopy's message display
snoopy_message_placeholder_g4 = st.empty()

if st.button("Teach Snoopy a Shape! ▶️", key="snoopy_start_btn_g4"):
    st.session_state.snoopy_animation_started_g4 = True
    st.session_state.snoopy_current_message_index_g4 = 0 # Start from the first message
    scroll_to_top() # Scroll to top when starting Snoopy
    st.rerun()

if st.session_state.snoopy_animation_started_g4:
    # Loop through messages automatically
    if st.session_state.snoopy_current_message_index_g4 < len(snoopy_messages_g4):
        current_msg = snoopy_messages_g4[st.session_state.snoopy_current_message_index_g4]
        snoopy_message_placeholder_g4.markdown(f"<div class='lesson-card' style='background-color: #e0f8f0; text-align: center;'>🐶 {current_msg}</div>", unsafe_allow_html=True)
        time.sleep(3) # Pause for 3 seconds per message
        st.session_state.snoopy_current_message_index_g4 += 1
        st.rerun() # Rerun to show the next message
    else:
        # Animation finished
        st.success("See? Snoopy learned to recognize shapes! That's how AI gets smart! ✨")
        if st.button("Reset Snoopy", key="snoopy_reset_btn_final_g4"):
            st.session_state.snoopy_animation_started_g4 = False
            st.session_state.snoopy_current_message_index_g4 = 0
            scroll_to_top()
            st.rerun()
    
st.write("---")


# --- Chatbots: Your Talking Computer Friends! ---
st.header("💬 Chatbots: Your Talking Computer Friends! 🗣️💻")
st.markdown("""
<div class="lesson-card">
    <p>Chatbots: Your talking computer friends! 💬🤖</p>
    <p>They **CHAT** with you! They answer questions. They help you!</p>
    <p>Find them on websites, smart speakers, and games! 🎮</p>
    <p>In Grade 4, chatbots help in:</p>
    <ul>
        <li>**Smart homes** 🏠 (like turning on lights with your voice!)</li>
        <li>**Websites** helping grown-ups shop 🛒 (finding your favorite toys!)</li>
        <li>**Video games** where characters talk back! 🎮 (like quests in a magical world!)</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# --- Seeing is Believing: A Chatbot in Action! (Grade 4 - New Scenario) ---
st.subheader("Seeing is Believing: A Chatbot in Action! 👀")
st.markdown("""
<div class="lesson-card">
    <p>Let's see how a smart chatbot helps a student with their **school project**! 📚 Watch the conversation unfold! 👇</p>
</div>
""", unsafe_allow_html=True)

if st.button("Show Chatbot Conversation ▶️", key="simulated_chat_btn"):
    st.write("---")
    chat_placeholder = st.empty()
    chat_messages_g4_sim = [ # New, more advanced scenario for Grade 4
        {"role": "user", "content": "Hi! I need help with my science project on planets. 🪐"},
        {"role": "bot", "content": "Hello! I can help with that! Which planet are you curious about? 🤔"},
        {"role": "user", "content": "Tell me about Mars! 🔴"},
        {"role": "bot", "content": "Mars is called the Red Planet! It has two small moons and scientists are looking for water there! 🚀💧"},
        {"role": "user", "content": "Cool! What about Jupiter? 🌌"},
        {"role": "bot", "content": "Jupiter is the biggest planet! It has a giant red spot, which is a huge storm! 🌪️"},
        {"role": "user", "content": "Thanks, this is really helpful! 😊"},
        {"role": "bot", "content": "You're welcome! Keep exploring the universe! ✨"},
    ]

    current_chat_display = []
    for msg in chat_messages_g4_sim: # Using new messages
        if msg["role"] == "user":
            current_chat_display.append(f"<div class='simulated-chat-message-user'>👦 {msg['content']}</div>")
        else:
            current_chat_display.append(f"<div class='simulated-chat-message-bot'>🤖 {msg['content']}</div>")
        chat_placeholder.markdown("".join(current_chat_display), unsafe_allow_html=True)
        time.sleep(1.5)
    st.success("See! The chatbot helped with a school project! 🎉")
    st.write("---")
    scroll_to_top()


# --- The Magic Line of Code! (Grade 4: Two Commands with simplified explanations) ---
st.header("✨ The Magic Line of Code! �")
st.markdown("""
<div class="lesson-card">
    <p>Chatbots use secret code spells! 🧙‍♀️</p>
    <p>Here's how we tell the computer to make magic happen:</p>
</div>
""", unsafe_allow_html=True)

# Command 1: Print
st.subheader("Spell 1: Make the Computer Talk! 🗣️")
st.markdown("""
<div class="code-explanation">
    <p><b><code>print</code></b>: Show words on screen! 🖥️💬</p>
    <p>Words in "quotation marks" are what it says!</p>
</div>
""", unsafe_allow_html=True) # Simplified explanation
st.code("""
print("Hello, EduSpark learners!") # Make the computer say hello!
""", language="python")

if "code_output_1" not in st.session_state:
    st.session_state.code_output_1 = ""

if st.button("Run Spell 1 ▶️", key="run_magic_code_btn_1"):
    st.session_state.code_output_1 = "Hello, EduSpark learners!" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_1:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_1}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 1", key="clear_code_output_btn_1"):
        st.session_state.code_output_1 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---") # Separator between commands

# Command 2: String Concatenation
st.subheader("Spell 2: Combine Words! 🧩")
st.markdown("""
<div class="code-explanation">
    <p><b>Variables</b>: Special boxes for words! 📦</p>
    <p><b><code>+</code></b>: Sticks words together! 🔗</p>
    <p>This is how chatbots build replies! 💬</p>
</div>
""", unsafe_allow_html=True) # Simplified explanation
st.code("""
first_word = "Magic"
second_word = "Spells"
print(first_word + " " + second_word + "!") # Combine words for a new message!
""", language="python")

if "code_output_2" not in st.session_state:
    st.session_state.code_output_2 = ""

if st.button("Run Spell 2 ▶️", key="run_magic_code_btn_2"):
    st.session_state.code_output_2 = "Magic Spells!" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_2:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_2}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 2", key="clear_code_output_btn_2"):
        st.session_state.code_output_2 = ""
        scroll_to_top()
        st.rerun()

st.markdown("""
<div class="lesson-card">
    <p>See how we used two magic spells? ✨</p>
    <p>Chatbots use many spells like these to understand your questions and give you smart answers! 🤖💬</p>
</div>
""", unsafe_allow_html=True)


# --- Talk to the Harry Potter Chatbot! ---
st.header("⚡ Talk to the Harry Potter Chatbot! 🧙‍♂️🦉")
st.markdown("""
<div class="lesson-card">
    <p>Get ready to chat with Harry Potter! He's excited to answer your questions about Hogwarts, spells, and his magical adventures!</p>
</div>
""", unsafe_allow_html=True)

# Check if harry.png exists, otherwise use a placeholder
harry_image_path = "assets/harry.png" # Changed to assets/harry.png
if os.path.exists(harry_image_path):
    st.image(harry_image_path, caption="Meet Harry Potter!", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=Harry+Potter",
             caption="Meet Harry Potter! (Image not found: place 'harry.png' in your assets folder)",
             use_container_width=True)

# Initialize chat history for Harry Potter chatbot
if "harry_potter_messages" not in st.session_state:
    st.session_state.harry_potter_messages = []
    initial_greeting_content_hp = (
        "Greetings, young wizard! ✨ I'm Harry Potter. "
        "Ready to talk about Hogwarts, spells, or magical creatures? 🧙‍♂️🦉"
    )
    styled_initial_greeting_hp = f"""
    <div style="
        font-size: 26px; /* Larger font for greeting */
        background-color: #e6f7ff; /* Light blue background */
        padding: 15px;
        border-radius: 15px;
        text-align: left;
        margin-right: 25%; /* Align like bot message */
        box-shadow: -2px 2px 5px rgba(0,0,0,0.15);
    ">
        {initial_greeting_content_hp}
    </div>
    """
    st.session_state.harry_potter_messages.append({"role": "bot", "content": styled_initial_greeting_hp, "is_html": True})

# Initialize the current input value for the Harry Potter chatbot
if "current_harry_input" not in st.session_state:
    st.session_state.current_harry_input = ""

# Display chat messages from history using st.chat_message
for message in st.session_state.harry_potter_messages:
    with st.chat_message(message["role"]):
        if message.get("is_html"):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.write(message["content"])

st.markdown("""
<div class="lesson-card">
    <p>Click a button to ask Harry! 👇</p>
</div>
""", unsafe_allow_html=True)

# Sample questions as buttons for Harry Potter
sample_questions_hp = [
    "What's your favorite spell? ✨",
    "Who is your best friend? 🤝",
    "Tell me about Hogwarts! 🏰",
    "What's your favorite magical creature? 🐉",
]

cols_hp = st.columns(len(sample_questions_hp))
for i, question in enumerate(sample_questions_hp):
    with cols_hp[i]:
        if st.button(question, key=f"sample_hp_q_btn_{i}"):
            st.session_state.current_harry_input = question
            st.rerun()

# Changed to st.text_area for bigger input field
user_question_hp = st.text_area(
    "Or type your own question here for Harry:",
    value=st.session_state.current_harry_input,
    height=100, # Make the text area taller
    key="harry_chatbot_input_widget"
)

if st.button("Ask Harry! 🧙‍♂️", key="send_harry_message_btn"):
    if user_question_hp:
        st.session_state.harry_potter_messages.append({"role": "user", "content": user_question_hp})
        st.session_state.current_harry_input = ""

        with st.spinner("Harry is thinking... 🤔"):
            time.sleep(2)

            user_q_lower_hp = user_question_hp.lower()
            if "spell" in user_q_lower_hp:
                harry_response = "My favorite spell is Expelliarmus! It's super useful for disarming opponents! ✨"
            elif "friend" in user_q_lower_hp:
                harry_response = "Ron and Hermione are my best friends! We've had so many adventures together! 🤝"
            elif "hogwarts" in user_q_lower_hp:
                harry_response = "Hogwarts is the best! It's a magical school full of secrets, amazing classes, and delicious feasts! 🏰"
            elif "creature" in user_q_lower_hp:
                harry_response = "I love Buckbeak, the Hippogriff! They're magnificent creatures, but you have to be polite! 🦅"
            elif "hello" in user_q_lower_hp or "hi" in user_q_lower_hp:
                harry_response = "Hello there, young wizard! What magical question do you have for me today? 🦉"
            else:
                harry_response = "That's a fascinating question! The wizarding world holds many mysteries. Ask me something else about my adventures! 📚"
        
        st.session_state.harry_potter_messages.append({"role": "bot", "content": harry_response})
        st.rerun()
    else:
        st.warning("Oops! 🚨 Please type a question for Harry or click a sample button! 👇")

st.write("---")
st.success("You've completed the Grade 4 Chatbots lesson! Great job! 🏆")


# --- Navigation ---
if st.button("⬅️ Back to AI Learning Mode", key="back_to_ai_learning_from_g4"):
    st.switch_page("pages/2_AI_Learning_Mode.py")

# --- Sidebar Footer (always visible) ---
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ for the students of Pakistan! 🇵🇰")
