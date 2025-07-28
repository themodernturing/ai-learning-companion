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
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def scroll_to_top():
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

# --- Page Content ---
st.title("🌟 Grade 3: AI, Chatbots, & Fun! 🌟")
st.markdown("---")

# --- Welcome & What is AI? (Grade 3) ---
st.header("What is Artificial Intelligence? 🧠")
st.markdown("""
<div class="lesson-card">
    <p>**Artificial Intelligence (AI)**: Computers that can **THINK** and **LEARN**! 🤯</p>
    <p>It's like teaching a robot to be super smart and helpful. 🤖</p>
    <p>AI helps make cool games and smart toys! 🎮🤖 Learning about AI is super fun! ✨</p>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- AI is Everywhere! / Sparky (Grade 3 specific: Favorite Color) ---
st.header("AI is Everywhere! Can you spot it? 🕵️‍♀️")
st.markdown("""
<div class="lesson-card">
    <p>Let's meet **Sparky the Smart Toy!** 🧸💡 Sparky can learn your favorite things and even talk to you! That's AI magic! ✨</p>
    <p>We'll show you how Sparky learns your favorite color! 👇</p>
</div>
""", unsafe_allow_html=True)

# Initialize Sparky's state for automatic animation
if "sparky_animation_started_g3" not in st.session_state:
    st.session_state.sparky_animation_started_g3 = False
if "sparky_current_message_index_g3" not in st.session_state:
    st.session_state.sparky_current_message_index_g3 = 0

sparky_messages_g3 = [
    "You tell Sparky: 'My favorite color is **RED**!' 🗣️",
    "Sparky remembers your color! 🧠 (It's **RED**!)",
    "Now, you ask Sparky: 'What's my favorite color?' 🤔",
    "Sparky says: 'Your favorite color is **RED**!' 🎉",
]

# Placeholder for Sparky's message display
sparky_message_placeholder_g3 = st.empty()

if st.button("See Sparky in Action! ▶️", key="sparky_start_btn_g3"):
    st.session_state.sparky_animation_started_g3 = True
    st.session_state.sparky_current_message_index_g3 = 0 # Start from the first message
    scroll_to_top() # Scroll to top when starting Sparky
    st.rerun()

if st.session_state.sparky_animation_started_g3:
    # Loop through messages automatically
    if st.session_state.sparky_current_message_index_g3 < len(sparky_messages_g3):
        current_msg = sparky_messages_g3[st.session_state.sparky_current_message_index_g3]
        sparky_message_placeholder_g3.markdown(f"<div class='lesson-card' style='background-color: #e0f8f0; text-align: center;'>🧸 {current_msg}</div>", unsafe_allow_html=True)
        time.sleep(3) # Pause for 3 seconds per message (adjust as needed)
        st.session_state.sparky_current_message_index_g3 += 1
        st.rerun() # Rerun to show the next message
    else:
        # Animation finished
        st.success("See? Sparky learned something new from you! That's AI magic! ✨")
        if st.button("Reset Sparky", key="sparky_reset_btn_final_g3"):
            st.session_state.sparky_animation_started_g3 = False
            st.session_state.sparky_current_message_index_g3 = 0
            scroll_to_top()
            st.rerun()
    
st.write("---")


# --- Chatbots: Your Talking Computer Friends! ---
st.header("💬 Chatbots: Your Talking Computer Friends! 🗣️💻")
st.markdown("""
<div class="lesson-card">
    <p>Imagine talking to a computer just like a friend! 💬 That's a **chatbot**! 🤖</p>
    <p>They are super friendly and can answer your questions. 🤩</p>
    <p>Find them in:</p>
    <ul>
        <li>**Websites** 🌐</li>
        <li>**Smart speakers** 🔊</li>
        <li>**Games** 🎮</li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- Seeing is Believing: A Chatbot in Action! (Grade 3: Lost Toy) ---
st.subheader("Seeing is Believing: A Chatbot in Action! 👀")
st.markdown("""
<div class="lesson-card">
    <p>Let's see how a simple chatbot helps a child find their **lost toy**! 🧸 Watch the conversation unfold! 👇</p>
</div>
""", unsafe_allow_html=True)

if st.button("Show Chatbot Conversation ▶️", key="simulated_chat_btn_g3_lost_toy"):
    st.write("---")
    chat_placeholder = st.empty()
    chat_messages_g3_sim = [
        {"role": "user", "content": "Lost my teddy! 🧸 Can you help? 🙏"},
        {"role": "bot", "content": "Oh no! 😥 Where did you last see your teddy? 🤔"},
        {"role": "user", "content": "Park, near the slide! 🏞️🎢"},
        {"role": "bot", "content": "Got it! Checking lost & found. 🔍 One moment... ⏳"},
        {"role": "user", "content": "Thanks! 😊"},
        {"role": "bot", "content": "Good news! 🎉 Teddy found at park office! Pick up before 5 PM! 🥳"},
    ]
    current_chat_display = []
    for msg in chat_messages_g3_sim:
        if msg["role"] == "user":
            current_chat_display.append(f"<div class='simulated-chat-message-user'>👦 {msg['content']}</div>")
        else:
            current_chat_display.append(f"<div class='simulated-chat-message-bot'>🤖 {msg['content']}</div>")
        chat_placeholder.markdown("".join(current_chat_display), unsafe_allow_html=True)
        time.sleep(1.5)
    st.success("See! The chatbot helped find the toy! 🎉")
    st.write("---")
    scroll_to_top()


# --- The Magic Line of Code! (Grade 3: Print) ---
st.header("✨ The Magic Line of Code! 🪄")
st.markdown("""
<div class="lesson-card">
    <p>You saw how the chatbot talked. But how does it *show* its answer? 🤔 It uses a secret code spell!</p>
    <p>Here's how we tell the computer to make magic happen:</p>
</div>
""", unsafe_allow_html=True)

# Command 1: Print
st.subheader("Spell: Make the Computer Talk! 🗣️")
st.markdown("""
<div class="code-explanation">
    <p>This spell tells the computer to **show words** on the screen. It's like the computer saying something out loud!</p>
    <p>The word **<code>print</code>** is the magic word. What's inside the <b>quotation marks</b> is what the computer will say!</p>
</div>
""", unsafe_allow_html=True)
st.code("""
print("🌟") # Show a STAR!
""", language="python")

if "code_output_g3" not in st.session_state:
    st.session_state.code_output_g3 = ""

if st.button("Run Spell ▶️", key="run_magic_code_btn_g3"):
    st.session_state.code_output_g3 = "🌟" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_g3:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_g3}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">See? <code>print(\"🌟\")</code> is like telling the computer: 'Show a STAR!' 🌟</p>
        <p style="font-size: 1.0em;">Our chatbot uses a special version of this "print" spell to show you its answers, like giving you a little gift! 🎁 That one line is the heart of how our chatbot talks to the AI! ❤️</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output", key="clear_code_output_btn_g3"):
        st.session_state.code_output_g3 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---")


# --- Talk to the We Baby Bears Chatbot! ---
st.header("⚡ Talk to the We Baby Bears Chatbot! 🐻🐼🧊")
st.markdown("""
<div class="lesson-card">
    <p>Get ready to chat with Grizz, Panda, and Ice Bear! 🐻🐼🧊</p>
    <p>They are excited to talk to you and share their adventures. They love learning new things!</p>
</div>
""", unsafe_allow_html=True)

# Check if image exists, otherwise use a placeholder
we_baby_bears_image_path = "assets/Screenshot 2025-07-12 145557.png" # Assuming this is your We Baby Bears image
if os.path.exists(we_baby_bears_image_path):
    st.image(we_baby_bears_image_path, caption="Meet Grizz, Panda, and Ice Bear!", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=We+Baby+Bears",
             caption="Meet Grizz, Panda, and Ice Bear! (Image not found: place 'Screenshot 2025-07-12 145557.png' in your assets folder)",
             use_container_width=True)


# Initialize chat history for We Baby Bears chatbot
if "we_baby_bears_messages" not in st.session_state:
    st.session_state.we_baby_bears_messages = []
    initial_greeting = (
        "Hi, little adventurer! 👋 We're the We Baby Bears! 🐻🐼🧊 "
        "We love exploring new worlds and making friends. "
        "Ask us anything about our fun journeys! ✨"
    )
    styled_initial_greeting = f"""
    <div style="font-size: 26px; background-color: #e6f7ff; padding: 15px; border-radius: 15px; text-align: left; margin-right: 25%; box-shadow: -2px 2px 5px rgba(0,0,0,0.15);">
        {initial_greeting}
    </div>
    """
    st.session_state.we_baby_bears_messages.append({"role": "bot", "content": styled_initial_greeting, "is_html": True})

# Initialize the current input value in session state
if "current_bears_input" not in st.session_state:
    st.session_state.current_bears_input = ""

# Display chat messages from history
for message in st.session_state.we_baby_bears_messages:
    with st.chat_message(message["role"]):
        if message.get("is_html"):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.write(message["content"])

st.markdown("""
<div class="lesson-card">
    <p>Click a button to ask the bears! 👇</p>
</div>
""", unsafe_allow_html=True)

# Sample questions as buttons
sample_questions = [
    "What's your favorite snack? 🍎",
    "Tell me about your best adventure! 🗺️",
    "What do you like to do for fun? 🥳",
    "Can you tell me a joke? 😂",
]

cols = st.columns(len(sample_questions))
for i, question in enumerate(sample_questions):
    with cols[i]:
        if st.button(question, key=f"sample_q_btn_{i}"):
            st.session_state.current_bears_input = question # Populate input box
            st.rerun() # Rerun to show question in input box

# The text input now uses the session state value
user_question_bears = st.text_input(
    "Or type your own question here:",
    value=st.session_state.get("current_bears_input", ""), # Get value from session state
    key="bears_chatbot_input_widget"
)

if st.button("Ask the Bears! 💬", key="send_bears_message_btn"):
    if user_question_bears:
        st.session_state.we_baby_bears_messages.append({"role": "user", "content": user_question_bears})
        
        with st.spinner("The bears are thinking... 🤔"):
            time.sleep(2) # Simulate AI processing time

            user_q_lower = user_question_bears.lower()
            if "snack" in user_q_lower or "food" in user_q_lower:
                bears_response = "Grizz: Pancakes! 🥞 Panda: Bamboo shoots! 🎋 Ice Bear: Salmon! 🍣 So yummy! 😋"
            elif "adventure" in user_q_lower or "travel" in user_q_lower:
                bears_response = "Grizz: Our best was finding the portal! ✨ Panda: Visiting the land of talking animals! 🗣️🦊 Ice Bear: Flying on a giant bird! 🦅 So cool! 😎"
            elif "fun" in user_q_lower or "play" in user_q_lower:
                bears_response = "Grizz: Exploring new worlds! 🗺️ Panda: Drawing and selfies! 🎨🤳 Ice Bear: Cooking and karate! 🥋 Fun for everyone! 😄"
            elif "joke" in user_q_lower:
                bears_response = "Grizz: Why did the bear cross the road? 🐻➡️🛣️ Panda: To get to the other side! 😂 Ice Bear: That's an old one. Ice Bear knows better jokes. 😉"
            elif "hello" in user_q_lower or "hi" in user_q_lower:
                bears_response = "Hey there, friend! 👋 We're so happy you're here! What fun can we get into today? 🥳"
            elif "name" in user_q_lower:
                bears_response = "We're Grizz, Panda, and Ice Bear! Nice to meet you! 🤗"
            else:
                bears_response = "That's a super interesting question! 🤔 We're still learning about that. Can you ask us something else about our adventures or favorite things? ✨"
        
        st.session_state.we_baby_bears_messages.append({"role": "bot", "content": bears_response})
        st.session_state.current_bears_input = "" # Clear input after sending
        st.rerun()
    else:
        st.warning("Oops! 🚨 Please type a question for the bears or click a sample button! 👇")

st.write("---")
st.success("You've completed the Grade 3 lesson! Great job! 🏆")

# --- Navigation ---
if st.button("⬅️ Back to AI Learning Mode", key="back_to_ai_learning_from_g3"):
    st.switch_page("pages/2_AI_Learning_Mode.py")

# --- Sidebar Footer (always visible) ---
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ for the students of Pakistan! 🇵🇰")
