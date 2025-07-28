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
st.title("🌟 Grade 5: AI, Chatbots, & Logic! 🌟")
st.markdown("---")

# --- Welcome & What is AI? (Grade 5) ---
st.header("What is Artificial Intelligence? 🧠")
st.markdown("""
<div class="lesson-card">
    <p>**Artificial Intelligence (AI)**: Smart machines! 🧠💡 They **solve problems** and **make decisions**.</p>
    <p>AI learns from **data** (information) to get smarter. 📊</p>
    <p>It helps with things like recommending videos or powering smart homes! 🏠🎬</p>
    <p>AI is shaping our future! 🚀 Get ready to learn! 🌟</p>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- AI is Everywhere! / Wednesday Addams (Grade 5 specific: Logic & Patterns) ---
st.header("AI is Everywhere! Meet Wednesday Addams! 🕷️")
st.markdown("""
<div class="dark-lesson-card">
    <p>Wednesday Addams has a keen eye for **logic and patterns**. 🕸️ She observes, analyzes, and deduces. This is very much like how AI works!</p>
    <p>AI also observes **data**, finds **patterns**, and uses **logic** to make sense of the world. Let's see how AI, like Wednesday, can uncover hidden connections! 👇</p>
</div>
""", unsafe_allow_html=True)

# Check if Wednesday.jpg exists, otherwise use a placeholder
wednesday_image_path = "assets/Wednesday.jpg" # Assuming this is your Wednesday Addams image
if os.path.exists(wednesday_image_path):
    st.image(wednesday_image_path, caption="Wednesday Addams: Master of Logic!", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=Wednesday+Addams",
             caption="Wednesday Addams: Master of Logic! (Image not found: place 'Wednesday.jpg' in your assets folder)",
             use_container_width=True)

# Initialize Wednesday's state for automatic animation
if "wednesday_animation_started_g5" not in st.session_state:
    st.session_state.wednesday_animation_started_g5 = False
if "wednesday_current_message_index_g5" not in st.session_state:
    st.session_state.wednesday_current_message_index_g5 = 0

wednesday_messages_g5 = [
    "Wednesday observes a series of clues. 🕵️‍♀️",
    "She analyzes the sequence... 🧠",
    "She deduces the missing piece using logic! ✅",
    "Now, she applies the pattern to a new mystery! 🌑",
    "She correctly identifies the solution! 🎉",
]

# Placeholder for Wednesday's message display
wednesday_message_placeholder_g5 = st.empty()

if st.button("See Wednesday's Logic in Action! ▶️", key="wednesday_start_btn_g5"):
    st.session_state.wednesday_animation_started_g5 = True
    st.session_state.wednesday_current_message_index_g5 = 0 # Start from the first message
    scroll_to_top() # Scroll to top when starting Wednesday
    st.rerun()

if st.session_state.wednesday_animation_started_g5:
    # Loop through messages automatically
    if st.session_state.wednesday_current_message_index_g5 < len(wednesday_messages_g5):
        current_msg = wednesday_messages_g5[st.session_state.wednesday_current_message_index_g5]
        wednesday_message_placeholder_g5.markdown(f"<div class='dark-lesson-card' style='text-align: center;'>🕷️ {current_msg}</div>", unsafe_allow_html=True)
        time.sleep(3) # Pause for 3 seconds per message
        st.session_state.wednesday_current_message_index_g5 += 1
        st.rerun() # Rerun to show the next message
    else:
        # Animation finished
        st.success("Wednesday's logic is impeccable! That's how AI identifies patterns and solves problems! ✨")
        if st.button("Reset Wednesday's Logic", key="wednesday_reset_btn_final_g5"):
            st.session_state.wednesday_animation_started_g5 = False
            st.session_state.wednesday_current_message_index_g5 = 0
            scroll_to_top()
            st.rerun()
    
st.write("---")


# --- Chatbots: Your Talking Computer Friends! ---
st.header("💬 Chatbots: Your Talking Computer Friends! 🗣️💻")
st.markdown("""
<div class="lesson-card">
    <p>Chatbots are AI programs designed to simulate human conversation. They process your words and respond using rules or advanced learning. It's like a digital assistant! 🧑‍💻</p>
    <p>They help us quickly find information, solve problems, and even automate simple tasks like setting reminders! ⏰</p>
    <p>You can find them in:</p>
    <ul>
        <li>**Customer support** on websites 🌐</li>
        <li>**Virtual assistants** on phones 📱</li>
        <li>**Educational tools** like EduSpark! 📚</li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- Seeing is Believing: A Chatbot in Action! (Grade 5 - New Scenario) ---
st.subheader("Seeing is Believing: A Chatbot in Action! 👀")
st.markdown("""
<div class="lesson-card">
    <p>Let's see how a chatbot helps **Wednesday and Enid** plan their next outing! 🕷️🌈 Watch the conversation unfold! 👇</p>
</div>
""", unsafe_allow_html=True)

if st.button("Show Chatbot Conversation ▶️", key="simulated_chat_btn_g5"):
    st.write("---")
    chat_placeholder = st.empty()
    chat_messages_g5_sim = [
        {"role": "user", "content": "Enid: Hey Wednesday! Want to go to the carnival? 🎡"},
        {"role": "bot", "content": "Wednesday: Carnivals are a cacophony of manufactured joy. However, I am intrigued by the potential for existential dread. What time? 🕰️"},
        {"role": "user", "content": "Enid: Yay! How about 7 PM? And what should we wear? I was thinking bright colors! 🌈"},
        {"role": "bot", "content": "Wednesday: 7 PM is acceptable. Regarding attire, I shall wear black. You may wear whatever garish colors you deem appropriate for public consumption. 🖤"},
        {"role": "user", "content": "Enid: Awesome! See you there! Can't wait! 😄"},
        {"role": "bot", "content": "Wednesday: Indeed. Try not to spontaneously combust from excessive enthusiasm. 🕷️"},
    ]
    current_chat_display = []
    for msg in chat_messages_g5_sim:
        if msg["role"] == "user":
            current_chat_display.append(f"<div class='simulated-chat-message-user'>👧 {msg['content']}</div>") # Changed icon to girl
        else:
            current_chat_display.append(f"<div class='simulated-chat-message-bot'>🕷️ {msg['content']}</div>") # Changed icon to spider for Wednesday
        chat_placeholder.markdown("".join(current_chat_display), unsafe_allow_html=True)
        time.sleep(1.5)
    st.success("See! Even Wednesday and Enid can use a chatbot... in their own unique way! 🎉")
    st.write("---")
    scroll_to_top()


# --- The Magic Line of Code! (Grade 5: Three Commands) ---
st.header("✨ The Magic Line of Code! 🪄")
st.markdown("""
<div class="lesson-card">
    <p>Chatbots use powerful code spells to work their magic! 🧙‍♀️</p>
    <p>Here's how we tell the computer to make magic happen:</p>
</div>
""", unsafe_allow_html=True)

# Command 1: Print
st.subheader("Spell 1: Display Messages! 🗣️")
st.markdown("""
<div class="code-explanation">
    <p><b><code>print()</code></b>: This command displays text on the screen. It's how the chatbot "talks" to you!</p>
    <p>Anything inside the parentheses and quotation marks will be shown.</p>
</div>
""", unsafe_allow_html=True)
st.code("""
print("Welcome, future AI innovators!") # Display a greeting
""", language="python")

if "code_output_1_g5" not in st.session_state:
    st.session_state.code_output_1_g5 = ""

if st.button("Run Spell 1 ▶️", key="run_magic_code_btn_1_g5"):
    st.session_state.code_output_1_g5 = "Welcome, future AI innovators!" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_1_g5:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_1_g5}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">This shows the text directly on the screen, just like a chatbot talking to you! 💬</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 1", key="clear_code_output_btn_1_g5"):
        st.session_state.code_output_1_g5 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---")

# Command 2: Variables (Strings and Numbers)
st.subheader("Spell 2: Store Information! 📦")
st.markdown("""
<div class="code-explanation">
    <p><b>Variables</b> are like named containers or boxes that hold information (data).</p>
    <p>You can store **words** (called "strings") or **numbers** in them. This is how a chatbot remembers things!</p>
    <p>Example: `name = "Tony"` (a string) or `age = 10` (a number).</p>
</div>
""", unsafe_allow_html=True)
st.code("""
character_name = "Wednesday"
mystery_solved = 7
print(character_name)
print(mystery_solved)
""", language="python")

if "code_output_2_g5" not in st.session_state:
    st.session_state.code_output_2_g5 = ""

if st.button("Run Spell 2 ▶️", key="run_magic_code_btn_2_g5"):
    st.session_state.code_output_2_g5 = "Wednesday\n7" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_2_g5:
    # Perform the replacement outside the f-string to avoid potential syntax issues
    output_with_br = st.session_state.code_output_2_g5.replace('\n', '<br>')
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{output_with_br}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">
            The output shows the information stored in our variables:
            <br><b>"Wednesday"</b> is the value of `character_name`.
            <br><b>"7"</b> is the value of `mystery_solved`.
            <br>This is how a computer remembers different pieces of information! 🧠
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 2", key="clear_code_output_btn_2_g5"):
        st.session_state.code_output_2_g5 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---")

# Command 3: Simple Arithmetic
st.subheader("Spell 3: Do Math! ➕➖")
st.markdown("""
<div class="code-explanation">
    <p>Computers are super fast at doing math! You can use them to add, subtract, multiply, and divide numbers.</p>
    <p>This helps chatbots calculate things, like scores in a game or totals in a shop.</p>
</div>
""", unsafe_allow_html=True)
st.code("""
clues_found = 10
clues_remaining = 3
total_clues = clues_found + clues_remaining
print(total_clues) # What's the total?
""", language="python")

if "code_output_3_g5" not in st.session_state:
    st.session_state.code_output_3_g5 = ""

if st.button("Run Spell 3 ▶️", key="run_magic_code_btn_3_g5"):
    st.session_state.code_output_3_g5 = "13" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_3_g5:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_3_g5}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">
            The output **{st.session_state.code_output_3_g5}** is the sum of `clues_found` (10) and `clues_remaining` (3).
            <br>This shows how computers can quickly do calculations for us! 🧮
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 3", key="clear_code_output_btn_3_g5"):
        st.session_state.code_output_3_g5 = ""
        scroll_to_top()
        st.rerun()

st.markdown("""
<div class="lesson-card">
    <p>See how computers use these spells to be smart? ✨</p>
    <p>Chatbots use many spells like these to understand your questions and give you smart answers! 🤖💬</p>
</div>
""", unsafe_allow_html=True)

st.write("---")


# --- Talk to the Wednesday Addams Chatbot! ---
st.header("⚡ Talk to the Wednesday Addams Chatbot! 🕷️")
st.markdown("""
<div class="dark-lesson-card">
    <p>Prepare to engage with **Wednesday Addams!** 🕷️ She appreciates logical inquiries and direct questions. Avoid frivolity.</p>
</div>
""", unsafe_allow_html=True)

# Check if Wednesday.jpg exists, otherwise use a placeholder
wednesday_image_path_chat = "assets/Wednesday.jpg" # Assuming this is your Wednesday Addams image
if os.path.exists(wednesday_image_path_chat):
    st.image(wednesday_image_path_chat, caption="Talk to Wednesday Addams!", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=Wednesday+Addams",
             caption="Talk to Wednesday Addams! (Image not found: place 'Wednesday.jpg' in your assets folder)",
             use_container_width=True)

# Initialize chat history for Wednesday Addams chatbot
if "wednesday_addams_messages" not in st.session_state:
    st.session_state.wednesday_addams_messages = []
    initial_greeting_content_wa = (
        "Greetings. I am Wednesday Addams. "
        "State your purpose. Or, if you must, ask a question. 🕷️"
    )
    styled_initial_greeting_wa = f"""
    <div style="font-size: 26px; background-color: #333333; color: #f0f0f0; padding: 15px; border-radius: 15px; text-align: left; margin-right: 25%; box-shadow: -2px 2px 5px rgba(0,0,0,0.15);">
        {initial_greeting_content_wa}
    </div>
    """
    st.session_state.wednesday_addams_messages.append({"role": "bot", "content": styled_initial_greeting_wa, "is_html": True})

# Initialize the current input value for the Wednesday Addams chatbot
if "current_wednesday_input" not in st.session_state:
    st.session_state.current_wednesday_input = ""

# Display chat messages from history using st.chat_message
for message in st.session_state.wednesday_addams_messages:
    with st.chat_message(message["role"]):
        if message.get("is_html"):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.write(message["content"])

st.markdown("""
<div class="dark-lesson-card">
    <p>Click a button to ask Wednesday! 👇</p>
</div>
""", unsafe_allow_html=True)

# Sample questions as buttons for Wednesday Addams
sample_questions_wa = [
    "What's your favorite mystery? 🔍",
    "Tell me about Nevermore Academy. 🦉",
    "What do you think of human emotions? 😐",
    "Can you tell me a logical riddle? 🧩",
]

cols_wa = st.columns(len(sample_questions_wa))
for i, question in enumerate(sample_questions_wa):
    with cols_wa[i]:
        if st.button(question, key=f"sample_wa_q_btn_{i}"):
            st.session_state.current_wednesday_input = question
            st.rerun()

# Changed to st.text_area for bigger input field
user_question_wa = st.text_area(
    "Or type your own question here for Wednesday:",
    value=st.session_state.current_wednesday_input,
    height=100, # Make the text area taller
    key="wednesday_addams_chatbot_input_widget"
)

if st.button("Ask Wednesday! 🕷️", key="send_wednesday_message_btn"):
    if user_question_wa:
        st.session_state.wednesday_addams_messages.append({"role": "user", "content": user_question_wa})
        st.session_state.current_wednesday_input = ""

        with st.spinner("Wednesday is contemplating... 🤔"):
            time.sleep(2)

            user_q_lower_wa = user_question_wa.lower()
            if "mystery" in user_q_lower_wa:
                wednesday_response = "My favorite mystery involves uncovering the truth behind the monster at Nevermore. It required meticulous deduction. 🕸️"
            elif "nevermore academy" in user_q_lower_wa:
                wednesday_response = "Nevermore Academy is a place for outcasts, where I can hone my skills and perhaps, occasionally, tolerate others. It has its... moments. 🦉"
            elif "human emotions" in user_q_lower_wa:
                wednesday_response = "Human emotions are often illogical and messy. They tend to complicate simple matters. I find clarity in their absence. 😐"
            elif "logical riddle" in user_q_lower_wa:
                wednesday_response = "What has an eye, but cannot see? A needle. Simple, yet effective. 🧵"
            elif "hello" in user_q_lower_wa or "hi" in user_q_lower_wa:
                wednesday_response = "Your greeting is noted. Proceed with your inquiry. 🕷️"
            else:
                wednesday_response = "Your question lacks a certain... morbid curiosity. Perhaps a more direct line of inquiry would yield a more satisfactory response. 🌑"
        
        st.session_state.wednesday_addams_messages.append({"role": "bot", "content": wednesday_response})
        st.rerun()
    else:
        st.warning("Oops! 🚨 Please type a question for Wednesday or click a sample button! 👇")

st.write("---")
st.success("You've completed the Grade 5 Chatbots lesson! Great job! 🏆")


# --- Navigation ---
if st.button("⬅️ Back to AI Learning Mode", key="back_to_ai_learning_from_g5"):
    st.switch_page("pages/2_AI_Learning_Mode.py")

# --- Sidebar Footer (always visible) ---
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ for the students of Pakistan! 🇵🇰")
