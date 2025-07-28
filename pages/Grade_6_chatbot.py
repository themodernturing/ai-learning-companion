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
st.title("🌟 Grade 6: AI, Logic, & Future Innovations! 🌟")
st.markdown("---")

# --- Welcome & What is AI? (Grade 6) ---
st.header("What is Artificial Intelligence? 🧠")
st.markdown("""
<div class="lesson-card">
    <p>**Artificial Intelligence (AI)**: Machines that can **think, learn, and act** like humans! 🤖🧠</p>
    <p>They learn from **huge amounts of data** to find patterns and make predictions. 📈</p>
    <p>AI drives innovation in science, medicine, and technology. 🔬🚗</p>
    <p>It's about creating intelligent systems that can **solve complex challenges** and **change the world**! 🌍✨</p>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- AI is Everywhere! / Elon Musk (Grade 6 specific: Innovation & Future) ---
st.header("AI is Everywhere! Inspired by Elon Musk! 🚀")
st.markdown("""
<div class="lesson-card">
    <p>Visionaries like **Elon Musk** are pushing the boundaries of what's possible with technology and AI! 💡🌍</p>
    <p>He famously said: **"When something is important enough, you do it even if the odds are not in your favor."** ✨</p>
    <p>AI is a powerful tool for innovation. It helps us **solve big problems** and **create new possibilities**!</p>
    <p>Think about how AI is used in self-driving cars 🚗, space exploration 🚀, and even brain-computer interfaces 🧠!</p>
</div>
""", unsafe_allow_html=True)

# Check if Elon.jpg exists, otherwise use a placeholder
elon_musk_image_path = "assets/Elon.jpg" # Corrected to .jpg
if os.path.exists(elon_musk_image_path):
    st.image(elon_musk_image_path, caption="Elon Musk: A Visionary Innovator", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=Elon+Musk",
             caption="Elon Musk: A Visionary Innovator (Image not found: place 'Elon.jpg' in your assets folder)",
             use_container_width=True)
    
st.write("---")


# --- Chatbots: Your Talking Computer Friends! ---
st.header("💬 Chatbots: Your Talking Computer Friends! 🗣️💻")
st.markdown("""
<div class="lesson-card">
    <p>**Chatbots**: AI-powered conversational agents! 💬🤖</p>
    <p>They use **Natural Language Processing (NLP)** to understand human language. 🗣️</p>
    <p>They learn from vast amounts of **text data** to generate relevant and helpful responses. 📚</p>
    <p>You can find them in:</p>
    <ul>
        <li>**Customer service** (helping millions online) 📞</li>
        <li>**Virtual assistants** (like Siri or Alexa) 🔊</li>
        <li>**Educational tools** (like EduSpark helping you learn AI!) 🎓</li>
    </ul>
    <p>They are designed to mimic human conversation and provide efficient solutions. ✨</p>
</div>
""", unsafe_allow_html=True)
st.write("---")


# --- Seeing is Believing: A Chatbot in Action! (Grade 6 - Elon Musk & Donald Trump) ---
st.subheader("Seeing is Believing: A Chatbot in Action! 👀")
st.markdown("""
<div class="lesson-card">
    <p>Let's imagine a conversation between **Elon Musk** and **Donald Trump** about the future of AI! 🚀🇺🇸 Watch their unique perspectives unfold! 👇</p>
</div>
""", unsafe_allow_html=True)

if st.button("Show Visionary Conversation ▶️", key="simulated_chat_btn_g6"):
    st.write("---")
    chat_placeholder = st.empty()
    chat_messages_g6_sim = [
        {"role": "user", "content": "Elon Musk: Donald, the future of AI is about accelerating humanity towards a multi-planetary existence. What are your thoughts on its impact on Earth? 🚀"},
        {"role": "bot", "content": "Donald Trump: Elon, nobody builds better AI than us, believe me. It's going to be tremendous, the best AI, truly great. We'll use it to make America great again, the greatest. 🇺🇸"},
        {"role": "user", "content": "Elon Musk: But the ethical implications, the potential for superintelligence... we need robust regulatory frameworks to ensure beneficial AI. What's your strategy for governance? 🧠"},
        {"role": "bot", "content": "Donald Trump: We're going to have the smartest people, the best people, working on it. Nobody knows more about smart people than me. We'll make sure it's fair, very fair, to everyone. It's going to be huge. 👍"},
        {"role": "user", "content": "Elon Musk: And the workforce? Automation will displace many jobs. How do we transition society to a future where AI handles much of the labor? 🏭"},
        {"role": "bot", "content": "Donald Trump: We'll create jobs, the best jobs, like nobody's ever seen. AI will help us bring back manufacturing, make our industries stronger. It's going to be a beautiful thing for American workers. 💼"},
        {"role": "user", "content": "Elon Musk: The ambition is commendable. However, the scale of this technological shift demands a global, collaborative approach, not just nationalistic focus. 🌍"},
        {"role": "bot", "content": "Donald Trump: Look, we're going to win so much with AI, you're going to get tired of winning. It's going to be the biggest win, frankly, the biggest win in history. Nobody wins like us. 🏆"},
    ]
    current_chat_display = []
    for msg in chat_messages_g6_sim:
        if msg["role"] == "user":
            current_chat_display.append(f"<div class='simulated-chat-message-user'>👨‍🚀 {msg['content']}</div>") # Elon Musk icon
        else:
            current_chat_display.append(f"<div class='simulated-chat-message-bot'>👔 {msg['content']}</div>") # Donald Trump icon
        chat_placeholder.markdown("".join(current_chat_display), unsafe_allow_html=True)
        time.sleep(2.5) # Increased pause for more thoughtful conversation
    st.success("A truly... unique discussion on the future of AI! �")
    st.write("---")
    scroll_to_top()


# --- The Magic Line of Code! (Grade 6: Three Commands with detailed explanations) ---
st.header("✨ The Magic Line of Code! 🪄")
st.markdown("""
<div class="lesson-card">
    <p>Chatbots use advanced code spells to work their magic! 🧙‍♀️</p>
    <p>Here's how we tell the computer to make magic happen:</p>
</div>
""", unsafe_allow_html=True)

# Command 1: Print
st.subheader("Spell 1: Output Information! 🗣️")
st.markdown("""
<div class="code-explanation">
    <p><b><code>print()</code></b>: This fundamental command outputs information to the console or screen. It's how a program communicates results or messages to the user.</p>
    <p>Anything within the parentheses will be displayed. For text, it must be enclosed in quotation marks.</p>
</div>
""", unsafe_allow_html=True)
st.code("""
print("Hello, future AI architects!") # Display a greeting
""", language="python")

if "code_output_1_g6" not in st.session_state:
    st.session_state.code_output_1_g6 = ""

if st.button("Run Spell 1 ▶️", key="run_magic_code_btn_1_g6"):
    st.session_state.code_output_1_g6 = "Hello, future AI architects!"
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_1_g6:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_1_g6}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">This output directly displays the string "Hello, future AI architects!". It's how programs communicate with users. 💬</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 1", key="clear_code_output_btn_1_g6"):
        st.session_state.code_output_1_g6 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---")

# Command 2: Variables (Data Types: String, Integer, Float)
st.subheader("Spell 2: Store Complex Information! 📦")
st.markdown("""
<div class="code-explanation">
    <p><b>Variables</b> are named storage locations for data. In programming, data comes in different **types**:</p>
    <ul>
        <li><b>String (`str`)</b>: Text (e.g., `"Hello"`).</li>
        <li><b>Integer (`int`)</b>: Whole numbers (e.g., `10`).</li>
        <li><b>Float (`float`)</b>: Numbers with decimal points (e.g., `3.14`).</li>
    </ul>
    <p>Understanding data types is crucial for handling information accurately in AI systems.</p>
</div>
""", unsafe_allow_html=True)
st.code("""
project_name = "SpaceX Launch" # String
rockets_launched = 100         # Integer
success_rate = 98.7            # Float
print(project_name)
print(rockets_launched)
print(success_rate)
""", language="python")

if "code_output_2_g6" not in st.session_state:
    st.session_state.code_output_2_g6 = ""

if st.button("Run Spell 2 ▶️", key="run_magic_code_btn_2_g6"):
    st.session_state.code_output_2_g6 = "SpaceX Launch\n100\n98.7" # Simulate the output
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_2_g6:
    output_lines = st.session_state.code_output_2_g6.split('\n')
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">
            {output_lines[0]} <span style="font-size:0.8em; color:#555;">(String: text data)</span><br>
            {output_lines[1]} <span style="font-size:0.8em; color:#555;">(Integer: whole number data)</span><br>
            {output_lines[2]} <span style="font-size:0.8em; color:#555;">(Float: decimal number data)</span>
        </p>
        <p style="font-size: 1.0em; margin-top: 10px;">
            This output demonstrates how variables store different types of data (text, whole numbers, and decimal numbers).
            <br>AI models rely on these data types to process information effectively! 🧠📊
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 2", key="clear_code_output_btn_2_g6"):
        st.session_state.code_output_2_g6 = ""
        scroll_to_top()
        st.rerun()

st.markdown("---")

# Command 3: Conditional Logic (If/Else)
st.subheader("Spell 3: Make Decisions! 🚦")
st.markdown("""
<div class="code-explanation">
    <p><b>Conditional logic (`if`/`else`)</b> allows programs to make decisions based on whether a condition is true or false.</p>
    <p>This is fundamental to AI, enabling chatbots to respond differently based on user input, or self-driving cars to react to traffic conditions.</p>
</div>
""", unsafe_allow_html=True)
st.code("""
mars_mission_ready = True
if mars_mission_ready:
    print("Initiating Mars colonization plans! 🚀")
else:
    print("Further development needed for Mars mission. 🛠️")
""", language="python")

if "code_output_3_g6" not in st.session_state:
    st.session_state.code_output_3_g6 = ""

if st.button("Run Spell 3 ▶️", key="run_magic_code_btn_3_g6"):
    # Simulate output based on the hardcoded mars_mission_ready
    if True: # Since mars_mission_ready is hardcoded as True
        st.session_state.code_output_3_g6 = "Initiating Mars colonization plans! 🚀"
    else:
        st.session_state.code_output_3_g6 = "Further development needed for Mars mission. 🛠️"
    scroll_to_top()
    st.rerun()

if st.session_state.code_output_3_g6:
    st.markdown(f"""
    <div class="lesson-card" style="background-color: #e0f8f0; border: 2px solid var(--primary-blue);">
        <h4>Output:</h4>
        <p style="font-family: monospace; font-size: 1.1em;">{st.session_state.code_output_3_g6}</p>
        <p style="font-size: 1.0em; margin-top: 10px;">
            Because `mars_mission_ready` was set to `True`, the `if` condition was met, and the program decided to "Initiate Mars colonization plans!".
            <br>This demonstrates how AI uses logic to make different choices and respond dynamically! ✅
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Clear Output 3", key="clear_code_output_btn_3_g6"):
        st.session_state.code_output_3_g6 = ""
        scroll_to_top()
        st.rerun()

st.markdown("""
<div class="lesson-card">
    <p>See how computers use these spells to be smart? ✨</p>
    <p>Chatbots use many spells like these to understand your questions and give you smart answers! 🤖💬</p>
</div>
""", unsafe_allow_html=True)

st.write("---")


# --- Talk to the Interactive Chatbot! (Elon Musk themed) ---
st.header("⚡ Talk to the Elon Musk Chatbot! 🚀")
st.markdown("""
<div class="lesson-card">
    <p>Get ready to chat with **Elon Musk!** 🚀 He's eager to discuss space, electric vehicles, AI, and the future of humanity!</p>
</div>
""", unsafe_allow_html=True)

# Check if Elon.jpg exists, otherwise use a placeholder
elon_image_path_chat = "assets/Elon.jpg" # Corrected to .jpg
if os.path.exists(elon_image_path_chat):
    st.image(elon_image_path_chat, caption="Talk to Elon Musk!", use_container_width=True)
else:
    st.image("https://placehold.co/400x400/000000/FFFFFF?text=Elon+Musk",
             caption="Talk to Elon Musk! (Image not found: place 'Elon.jpg' in your assets folder)",
             use_container_width=True)

# Initialize chat history for Elon Musk chatbot
if "elon_musk_messages" not in st.session_state:
    st.session_state.elon_musk_messages = []
    initial_greeting_content_em = (
        "Greetings, fellow innovator! 🚀 I'm Elon. "
        "Ready to discuss colonizing Mars, sustainable energy, or the future of AI? 🤔"
    )
    styled_initial_greeting_em = f"""
    <div style="font-size: 26px; background-color: #e6f7ff; padding: 15px; border-radius: 15px; text-align: left; margin-right: 25%; box-shadow: -2px 2px 5px rgba(0,0,0,0.15);">
        {initial_greeting_content_em}
    </div>
    """
    st.session_state.elon_musk_messages.append({"role": "bot", "content": styled_initial_greeting_em, "is_html": True})

# Initialize the current input value for the Elon Musk chatbot
if "current_elon_input" not in st.session_state:
    st.session_state.current_elon_input = ""

# Display chat messages from history using st.chat_message
for message in st.session_state.elon_musk_messages:
    with st.chat_message(message["role"]):
        if message.get("is_html"):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.write(message["content"])

st.markdown("""
<div class="lesson-card">
    <p>Click a button to ask Elon! 👇</p>
</div>
""", unsafe_allow_html=True)

# Sample questions as buttons for Elon Musk
sample_questions_em = [
    "Tell me about Mars colonization. 🔴",
    "What's the future of electric cars? 🚗",
    "How does AI impact space travel? 🌌",
    "What is Neuralink? 🧠",
]

cols_em = st.columns(len(sample_questions_em))
for i, question in enumerate(sample_questions_em):
    with cols_em[i]:
        if st.button(question, key=f"sample_em_q_btn_{i}"):
            st.session_state.current_elon_input = question
            st.rerun()

# Changed to st.text_area for bigger input field
user_question_em = st.text_area(
    "Or type your own question here for Elon:",
    value=st.session_state.current_elon_input,
    height=100, # Make the text area taller
    key="elon_musk_chatbot_input_widget"
)

if st.button("Ask Elon! 💬", key="send_elon_message_btn"):
    if user_question_em:
        st.session_state.elon_musk_messages.append({"role": "user", "content": user_question_em})
        st.session_state.current_elon_input = ""

        with st.spinner("Elon is thinking... 🤔"):
            time.sleep(2)

            user_q_lower_em = user_question_em.lower()
            if "mars colonization" in user_q_lower_em or "mars" in user_q_lower_em:
                elon_response = "Colonizing Mars is essential for humanity's long-term survival and expansion. We need to become a multi-planetary species to ensure our future. 🚀"
            elif "electric cars" in user_q_lower_em or "tesla" in user_q_lower_em:
                elon_response = "The future of electric cars is bright! They are crucial for sustainable energy and will eventually dominate the automotive industry. Tesla is leading the way. ⚡"
            elif "ai impact space travel" in user_q_lower_em or "ai space" in user_q_lower_em:
                elon_response = "AI is vital for autonomous spacecraft, complex mission planning, and data analysis in space travel. It enables us to explore further and more efficiently. 🌌"
            elif "neuralink" in user_q_lower_em:
                elon_response = "Neuralink aims to create a high-bandwidth brain-machine interface to help with neurological disorders and eventually achieve symbiotic AI. It's about expanding human capability. 🧠"
            elif "hello" in user_q_lower_em or "hi" in user_q_lower_em:
                elon_response = "Greetings. Ready to discuss the future? 💡"
            else:
                elon_response = "That's an interesting query. We're focused on accelerating the transition to sustainable energy and making humanity multi-planetary. Perhaps another question along those lines? 🤔"
        
        st.session_state.elon_musk_messages.append({"role": "bot", "content": elon_response})
        st.rerun()
    else:
        st.warning("Oops! 🚨 Please type a question for Elon or click a sample button! 👇")

st.write("---")
st.success("You've completed the Grade 6 Chatbots lesson! Great job! 🏆")


# --- Navigation ---
if st.button("⬅️ Back to AI Learning Mode", key="back_to_ai_learning_from_g6"):
    st.switch_page("pages/2_AI_Learning_Mode.py")

# --- Sidebar Footer (always visible) ---
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ for the students of Pakistan! 🇵🇰")
