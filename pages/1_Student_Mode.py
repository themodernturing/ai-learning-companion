import streamlit as st
import openai
import random
import re
import json # Import json for parsing AI responses
import time # For retry mechanism
import os # Import os to access environment variables

# ——— Page Configuration ———
st.set_page_config(page_title="AI Learning Companion", layout="wide")

# —— Optional CSS for Styling ———
st.markdown("""
    <style>
    .title {
        font-size: 2.5rem;
        color: #3399ff;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    .answer-box {
        background: #eaffea;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .mcq-display-box { /* New style for MCQ display */
        background: #fff3cd; /* Light yellow background */
        border-left: 5px solid #ffc107; /* Amber border */
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem; /* Added margin-bottom for consistent spacing */
        font-size: 1.05rem;
    }
    .related-answer-box {
        background: #e0f7fa; /* Light blue background */
        border-left: 5px solid #00bcd4; /* Cyan border */
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-size: 1.05rem;
    }
    .correct-feedback {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        display: flex; /* For icon alignment */
        align-items: center;
        flex-direction: column; /* Stack content vertically */
        align-items: flex-start; /* Align content to the start */
    }
    .incorrect-feedback {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        display: flex; /* For icon alignment */
        align-items: center;
    }
    /* New style for Real-Life Example box */
    .real-life-example-box {
        background: #f3e5f5; /* Light purple background */
        border-left: 5px solid #ab47bc; /* Purple border */
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        font-size: 1.1rem;
        font-weight: bold; /* Make text bolder */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        width: 100%; /* Ensure it takes full width within its parent */
    }
    /* Button Styling */
    .stButton>button {
        background-color: #3399ff; /* Blue */
        color: white;
        padding: 10px 20px;
        border-radius: 12px; /* More rounded */
        border: none;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease; /* Smooth transitions */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 5px; /* Add some margin around buttons */
    }
    .stButton>button:hover {
        background-color: #2a7acc; /* Darker blue on hover */
        transform: translateY(-2px); /* Slight lift effect */
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    /* Custom CSS for horizontal button layout */
    /* This targets the container holding the columns for button groups */
    div.st-emotion-cache-1r6dm1z { /* This is the specific class for the columns container */
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start; /* Align buttons to the start */
        gap: 10px; /* Space between buttons */
    }
    /* Specific styling for single buttons to ensure left alignment */
    div[data-testid="stVerticalBlock"] > div > div > div > div.stButton {
        display: flex;
        justify-content: flex-start;
    }

    </style>
""", unsafe_allow_html=True)

# ——— Data Definitions ———
# Updated SAMPLE_QUESTIONS to be grade-specific
SAMPLE_QUESTIONS = {
    "Math": {
        "3": ["What is addition?", "How do I count to 100?", "What are basic shapes?"],
        "4": ["How do I multiply numbers?", "What are fractions?", "Explain perimeter."],
        "5": ["What are decimals?", "How do I divide with remainders?", "Explain angles."],
        "6": ["What is algebra?", "How do I calculate area of complex shapes?", "Explain ratios."]
    },
    "Science": {
        "3": ["Why is the sky blue?", "What are living things?", "How do plants grow?"],
        "4": ["What are the planets?", "How does rain happen?", "What is a food chain?"],
        "5": ["Explain photosynthesis.", "What is gravity?", "How do volcanoes erupt?"],
        "6": ["What is the water cycle?", "Explain ecosystems.", "What are cells?"]
    },
    "English": {
        "3": ["What is a noun?", "Can you tell me a story?", "What is the opposite of 'happy'?"],
        "4": ["What is a verb?", "What is an adjective?", "Give me a poem."],
        "5": ["Explain metaphors.", "What is a protagonist?", "How do I write a paragraph?"],
        "6": ["What is persuasive writing?", "Explain literary devices.", "How do I identify themes in a story?"]
    }
}

# Updated RELATED_TOPICS to be grade-specific
RELATED_TOPICS = {
    "Math": {
        "3": ["What is subtraction?", "Explain counting by tens.", "Tell me about circles."],
        "4": ["Explain division.", "Tell me about decimals.", "What is area?"],
        "5": ["What are percentages?", "How do I solve word problems?", "Explain volume."],
        "6": ["What are integers?", "How do I graph coordinates?", "Explain probability."]
    },
    "Science": {
        "3": ["What are animals?", "What is weather?", "Tell me about the sun."],
        "4": ["What is the water cycle?", "How do magnets work?", "What are different types of energy?"],
        "5": ["Explain the human body.", "What are states of matter?", "How does sound travel?"],
        "6": ["What is genetics?", "Explain chemical reactions.", "What is renewable energy?"]
    },
    "English": {
        "3": ["What is a sentence?", "Tell me about rhyming words.", "What are story characters?"],
        "4": ["What is a paragraph?", "Explain similes and metaphors.", "How do I write a letter?"],
        "5": ["What is a theme?", "Explain different genres of books.", "How do I write an essay outline?"],
        "6": ["What is figurative language?", "Explain point of view.", "How do I analyze a poem?"]
    }
}


# MCQS dictionary will now be dynamically populated, so it can be empty or removed.
MCQS = {}

# ——— Utility Functions ———
def clean_text(text: str) -> str:
    # This regex removes content between double dollar signs, typically used for LaTeX math.
    # Adjust if your LaTeX format is different.
    return re.sub(r'\\\$.*?\\\$', '', text)

@st.cache_data(show_spinner=False) # Cache the AI answer to reduce API calls
def get_ai_answer(prompt: str, grade: str, subject: str, api_key: str) -> str:
    """
    Gets a general AI answer for a given prompt, tailored by grade.
    """
    # Refined system prompt for grade-level differentiation
    system = (
        f"You are a friendly AI tutor for Grade {grade} students learning {subject}. "
        f"Explain concepts using vocabulary, sentence structures, and examples that are "
        f"perfectly suited for a Grade {grade} student. "
        f"Your answer should be concise. "
        # Dynamically add grade-specific instructions based on the selected grade
        + (
            "Use extremely simple words and very short sentences (max 2-3 sentences)." if grade == "3" else
            "Use simple words and short sentences (max 3-4 sentences)." if grade == "4" else
            "Introduce slightly more varied vocabulary and sentences (max 4-5 sentences)." if grade == "5" else
            "Introduce slightly more complex vocabulary and slightly longer, but still clear, sentences (max 5-6 sentences)."
        ) +
        " Always include relevant emojis. Provide the answer ONLY for Grade {grade}. Do NOT mention other grades."
    )
    client = openai.OpenAI(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role":"system","content":system}, {"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=150 # Increased max_tokens slightly to allow for more detailed grade-specific answers
        )
        return clean_text(resp.choices[0].message.content.strip())
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
        return "Sorry, I couldn't get an answer right now. Please check your API key or try again later."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "Sorry, something went wrong. Please try again."

@st.cache_data(show_spinner=False) # Cache the MCQ generation
def get_ai_mcq(prompt: str, grade: str, subject: str, api_key: str, retries=3) -> dict | None:
    """
    Generates a multiple-choice question using the OpenAI API based on the prompt.
    Includes a retry mechanism for robust JSON parsing.
    Returns a dictionary with 'question', 'options', 'answer', 'explanations'.
    """
    system = (
        f"You are an AI assistant that creates a single multiple-choice question "
        f"for a Grade {grade} student learning {subject}. "
        "The question should be based on the user's query. "
        "Provide exactly 3 options, the correct answer, and a very short, simple explanation for each option. "
        "Keep the question and options very short and easy to understand for kids. "
        "Format the output strictly as a JSON object with the following keys: "
        "'question' (string), 'options' (list of 3 strings), 'answer' (string, one of the options), "
        "'explanations' (object mapping each option string to its explanation string)."
    )
    client = openai.OpenAI(api_key=api_key)
    for i in range(retries):
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role":"system","content":system}, {"role":"user","content":f"Generate an MCQ about: {prompt}"}],
                temperature=0.7,
                max_tokens=200, # Adjusted max_tokens for concise JSON output
                response_format={"type": "json_object"} # Ensure JSON output
            )
            mcq_data = json.loads(resp.choices[0].message.content.strip())
            # Basic validation for the expected keys
            if all(k in mcq_data for k in ['question', 'options', 'answer', 'explanations']) and \
               isinstance(mcq_data['options'], list) and len(mcq_data['options']) == 3:
                
                # SHUFFLE MCQ OPTIONS HERE
                random.shuffle(mcq_data['options']) # Shuffle the options list
                
                return mcq_data
            else:
                # Suppress st.warning for retries, only show error if all fail
                if i == retries - 1:
                    st.error("Failed to generate a valid MCQ after multiple attempts.")
                else:
                    # Optional: Log to console for debugging, but don't show to user
                    print(f"Attempt {i+1}: AI did not return MCQ in expected format. Retrying...")
                time.sleep(1) # Wait a bit before retrying
        except openai.APIError as e:
            if i == retries - 1:
                st.error(f"OpenAI API Error generating MCQ: {e}.")
            else:
                print(f"Attempt {i+1}: OpenAI API Error generating MCQ: {e}. Retrying...")
            time.sleep(1)
        except json.JSONDecodeError:
            if i == retries - 1:
                st.error("Failed to decode JSON from AI for MCQ after multiple attempts.")
            else:
                print(f"Attempt {i+1}: Failed to decode JSON from AI for MCQ. Retrying...")
            time.sleep(1)
        except Exception as e:
            if i == retries - 1:
                st.error(f"An unexpected error occurred during MCQ generation: {e}.")
            else:
                print(f"Attempt {i+1}: An unexpected error occurred during MCQ generation: {e}. Retrying...")
            time.sleep(1)
    return None # Return None if all retries fail

@st.cache_data(show_spinner=False) # Cache the real-life example generation
def get_ai_real_life_example(topic: str, grade: str, subject: str, api_key: str) -> str:
    """
    Gets a short, real-life example for a given topic.
    """
    system = (
        f"You are a friendly AI tutor for Grade {grade} students learning {subject}. "
        "Provide a very short, simple, and relatable real-life example for the given topic. "
        "Keep it to one or two sentences, suitable for kids. Use emojis."
    )
    client = openai.OpenAI(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role":"system","content":system}, {"role":"user","content":f"Give a real-life example for: {topic}"}],
            temperature=0.7,
            max_tokens=80 # Adjusted max_tokens for concise example
        )
        return clean_text(resp.choices[0].message.content.strip())
    except openai.APIError as e:
        return "Couldn't fetch a real-life example right now."
    except Exception as e:
        return "Couldn't fetch a real-life example right now."


# ——— Page Header ———
st.markdown('<div class="title">🎉 Pakistan’s First AI Learning Companion 🎉</div>', unsafe_allow_html=True)

# --- Retrieve API Key from Environment Variable ———
api_key = os.getenv("OPENAI_API_KEY")

# --- API Key Check and Stop if Missing ———
if not api_key:
    st.error("🚨 OpenAI API Key not found! Please ensure it's set in your .env file.")
    st.stop() # Stop execution if API key is not provided


# ——— Grade & Subject Selectors ———
col1, col2 = st.columns([1,2])
with col1:
    grade = st.selectbox("Select Grade", ["", "3","4","5","6"])
with col2:
    # Changed st.radio to st.selectbox for subject to allow no default selection
    subject = st.selectbox("Pick Subject", ["", "Math","Science","English"], index=0) # index=0 makes "" the default

# ——— Initialize Session State ———
# Ensure all necessary session state variables are initialized
for key in ("question","answer","related","mcq","feedback","related_topic_answer", "selected_mcq_choice", "show_sample_questions", "display_app_content", "show_goodbye_message", "show_quiz_section", "show_real_life_example_section", "cached_real_life_example", "show_related_topics_section", "show_sample_questions_buttons"):
    if key not in st.session_state:
        # Initialize question and answer to empty strings, not True/None
        if key == "question" or key == "answer":
            st.session_state[key] = ""
        elif key == "show_sample_questions":
            st.session_state[key] = True # Default to showing sample questions
        elif key == "display_app_content":
            st.session_state[key] = True # Default to showing main app content
        elif key == "show_goodbye_message":
            st.session_state[key] = False # Default to not showing goodbye message
        elif key == "show_quiz_section": # New state for quiz visibility
            st.session_state[key] = False
        elif key == "show_real_life_example_section": # New state for real-life example visibility
            st.session_state[key] = False
        elif key == "cached_real_life_example": # Cache for real-life example content
            st.session_state[key] = None
        elif key == "show_related_topics_section": # New state for related topics visibility
            st.session_state[key] = False
        elif key == "show_sample_questions_buttons": # New state to control visibility of sample question buttons
            st.session_state[key] = False # Initially hide sample question buttons
        else:
            st.session_state[key] = None

# --- Handle Exit App message at the very top (now removed as we switch page) ———
# if st.session_state.get('show_goodbye_message', False):
#     st.success("Thank you for learning with us! Goodbye! 👋")
#     if st.button("🚀 Start New Learning Session", key="start_new_session_btn_goodbye"):
#         st.session_state.clear() # Clear all session state
#         st.rerun() # Force a rerun to restart the app
#     st.stop() # Stop further execution if not restarting


# --- Reset states when grade or subject changes ———
# This helps with the "True" in answer box issue and general state consistency
# Also ensures prev_subject is properly initialized to avoid defaulting to Math
if "prev_grade" not in st.session_state or st.session_state.prev_grade != grade or \
   "prev_subject" not in st.session_state or st.session_state.prev_subject != subject:
    st.session_state.question = "" # Set to empty string, not None, for text_input
    st.session_state.answer = "" # Set to empty string
    st.session_state.related = None
    st.session_state.mcq = None
    st.session_state.feedback = None
    st.session_state.related_topic_answer = None
    st.session_state.selected_mcq_choice = None
    st.session_state.show_sample_questions = True # Show samples again on subject/grade change (this is for the caption, now removed)
    st.session_state.display_app_content = True # Ensure content is displayed
    st.session_state.show_quiz_section = False # Reset quiz visibility
    st.session_state.show_real_life_example_section = False # Reset real-life example visibility
    st.session_state.cached_real_life_example = None # Clear cached example
    st.session_state.show_related_topics_section = False # Reset related topics visibility
    st.session_state.show_sample_questions_buttons = False # Hide sample question buttons on subject/grade change
    st.session_state.prev_grade = grade
    st.session_state.prev_subject = subject


# --- Main Application Content ———
if st.session_state.display_app_content:
    # Only show main content if both grade and subject are selected
    if grade and subject:
        # Separate section for Ask Your Own Question (now at the very top)
        st.markdown(
        '<span style="color:#3399ff; font-size:1.45rem; font-weight:700;">Type Your Question for the AI Tutor!</span>',
        unsafe_allow_html=True
    )

        

        # ——— Question Input ———
        user_q = st.text_input(
            "Ask Your Question (in English or Roman Urdu):", # Rephrased label
            value=st.session_state.question, # Use current session state question
            placeholder="E.g., 'What is gravity?' or 'What is a verb?'", # Updated placeholder
            key="input_q"
        )

        # ——— Ask Now Button and Sample Questions Button in a single row ———
        col_ask_now, col_sample_q = st.columns([0.2, 0.8]) # Adjust column width for buttons

        with col_ask_now:
            if st.button("✅ Ask Now!"):
                if user_q: # Ensure there's a question to ask
                    # Set the question in session state to the typed question
                    st.session_state.question = user_q 
                    with st.spinner("Getting your answer..."):
                        ans = get_ai_answer(user_q, grade, subject, api_key)
                    st.session_state.answer = ans
                    # Fetch related topics based on selected subject and grade
                    st.session_state.related = RELATED_TOPICS.get(subject, {}).get(grade, [])
                    
                    # Generate MCQ immediately after getting the answer
                    with st.spinner("Generating a quick quiz..."):
                        st.session_state.mcq = get_ai_mcq(user_q, grade, subject, api_key)

                    # Reset visibility flags for new question
                    st.session_state.show_quiz_section = False
                    st.session_state.show_real_life_example_section = False
                    st.session_state.show_related_topics_section = False # Hide related topics on new question
                    st.session_state.feedback = None # Reset feedback
                    st.session_state.related_topic_answer = None # Clear related topic answer when new main question is asked
                    st.session_state.selected_mcq_choice = None # Clear selected MCQ choice on new question
                    st.session_state.show_sample_questions_buttons = False # Hide sample questions buttons after a typed question is asked
                    st.session_state.cached_real_life_example = None # Clear cached example
                    st.rerun() # Force a rerun to ensure correct state is reflected for quiz button
                else:
                    st.warning("Please type a question before clicking 'Ask Now!'.")

        with col_sample_q:
            # New button to show/hide sample questions
            if st.button("📚Sample Questions", key="show_sample_q_btn"):
                st.session_state.show_sample_questions_buttons = not st.session_state.show_sample_questions_buttons # Toggle visibility
                st.rerun() # Force rerun to show/hide buttons


        # Sample Questions Section (now only shown when 'show_sample_questions_buttons' is True)
        if st.session_state.show_sample_questions_buttons: # Only show if this state is True
            st.markdown("---") # Add separator here to visually group input/ask button
            
            # Revert to direct button display for sample questions
            samples = SAMPLE_QUESTIONS.get(subject, {}).get(grade, [])
            
            if samples: # Only display buttons if there are samples for the selected grade/subject
                # Use st.columns for horizontal layout of sample question buttons
                num_cols = min(len(samples), 3) # Limit to 3 columns for better spacing on various screens
                cols = st.columns(num_cols)
                for i, q in enumerate(samples):
                    # When a sample question button is clicked
                    with cols[i % num_cols]: # Distribute buttons across columns
                        if st.button(q, key=f"sample_{i}"):
                            st.session_state.question = q # Set the question in session state
                            # Trigger the AI answer and MCQ generation directly here
                            with st.spinner(f"Getting answer for '{q}'..."):
                                ans = get_ai_answer(q, grade, subject, api_key)
                            st.session_state.answer = ans
                            # Fetch related topics based on selected subject and grade
                            st.session_state.related = RELATED_TOPICS.get(subject, {}).get(grade, [])
                            
                            # Quiz and Real-Life Example are initially hidden for a new question
                            st.session_state.show_quiz_section = False
                            st.session_state.show_real_life_example_section = False
                            st.session_state.show_related_topics_section = False # Hide related topics on new question
                            st.session_state.feedback = None
                            st.session_state.related_topic_answer = None
                            st.session_state.selected_mcq_choice = None
                            st.session_state.show_sample_questions_buttons = False # Hide sample questions buttons after one is clicked
                            st.session_state.cached_real_life_example = None # Clear cached example
                            # Generate MCQ immediately after getting the answer
                            with st.spinner("Generating a quick quiz..."):
                                st.session_state.mcq = get_ai_mcq(q, grade, subject, api_key)
                            st.rerun() # Force a rerun to ensure correct state is reflected for quiz button
            else:
                st.info(f"No sample questions available for Grade {grade} {subject} yet. Please ask your own question!")


        # ——— Display Answer, then conditionally show "Show Quick Quiz" button ———
        if st.session_state.answer:
            # Added a clear caption above the answer box
            st.markdown("### ✨ Here's your answer!") # New caption for the answer box
            # Added an emoji prefix to the answer box for attractiveness
            st.markdown(f'<div class="answer-box">💡 {st.session_state.answer}</div>', unsafe_allow_html=True)

            # Show "Show Quick Quiz" button if quiz is not yet visible AND an MCQ was successfully generated
            if st.session_state.mcq and not st.session_state.show_quiz_section:
                if st.button("📝 Show Quick Quiz", key="show_quiz_btn"):
                    st.session_state.show_quiz_section = True
                    st.rerun() # Rerun to display the quiz section
            elif st.session_state.mcq is None and st.session_state.answer: # Only show this if an answer is present but MCQ generation failed
                st.info("No quick quiz available for this topic yet. Try asking a different question or re-asking this one!")
                # If no quiz, and answer is present, show related topics button immediately, as there's no quiz/RLE flow
                if st.session_state.related and not st.session_state.show_related_topics_section and not st.session_state.related_topic_answer:
                    if st.button("📚 Show Related Topics", key="show_related_topics_after_no_quiz_btn"):
                        st.session_state.show_related_topics_section = True
                        st.rerun()


            # ——— MCQ Section (Conditionally displayed) ———
            if st.session_state.show_quiz_section and st.session_state.mcq:
                st.markdown("---")
                st.markdown("### 📝 Quick Quiz")
                # Apply the new styling to the MCQ section
                st.markdown(f'<div class="mcq-display-box">', unsafe_allow_html=True)
                mcq = st.session_state.mcq
                st.write(mcq["question"])
                
                # Use a unique and STABLE key for the radio button.
                # The key should change ONLY if the MCQ question itself changes.
                choice_key = f"mcq_radio_{mcq['question']}" 
                
                # Store the selected choice in session state
                # Ensure index is within bounds of options, default to 0 if not
                initial_index = 0
                if st.session_state.selected_mcq_choice in mcq["options"]:
                    initial_index = mcq["options"].index(st.session_state.selected_mcq_choice)

                current_choice = st.radio("Choose your answer:", mcq["options"], 
                                          key=choice_key, 
                                          index=initial_index)
                
                # Update selected_mcq_choice in session state immediately when radio button changes
                if current_choice != st.session_state.selected_mcq_choice:
                    st.session_state.selected_mcq_choice = current_choice
                    st.session_state.feedback = None # Clear feedback if selection changes
                    st.session_state.show_real_life_example_section = False # Hide real-life example if choice changes

                # The feedback should be displayed only after submission.
                if st.button("Submit Answer", key=f"mcq_submit_{choice_key}"):
                    if st.session_state.selected_mcq_choice:
                        st.session_state.feedback_text = mcq["explanations"].get(st.session_state.selected_mcq_choice)
                        
                        # Add congratulatory message and real-life example for correct answer
                        if st.session_state.selected_mcq_choice == mcq["answer"]:
                            congratulations = "🎉 Great job! That's the correct answer! 🎉"
                            st.session_state.feedback = f'<div class="correct-feedback">✅ {congratulations}<br><br>{st.session_state.feedback_text}</div>'
                            
                            # Get real-life example and store it
                            with st.spinner("Getting a real-life example..."):
                                st.session_state.cached_real_life_example = get_ai_real_life_example(mcq["question"], grade, subject, api_key)
                            # Set flag to show real-life example section to False initially, to be shown by button
                            st.session_state.show_real_life_example_section = False 
                            
                        else:
                            st.session_state.feedback = f'<div class="incorrect-feedback">❌ Oops! That\'s not quite right. <br><br>{st.session_state.feedback_text}</div>'
                            # CORRECTED TYPO HERE: st.session_session_state -> st.session_state
                            st.session_state.show_real_life_example_section = False # Hide real-life example if incorrect
                            st.session_state.cached_real_life_example = None # Clear cached example
                    # Always rerun after submit to update feedback and potentially show real-life example button
                    st.rerun() 

                # Display feedback if it.session_state.feedback exists in session state
                if st.session_state.feedback:
                    st.markdown(st.session_state.feedback, unsafe_allow_html=True)
                    # Display "Show Real-Life Example" button only if answer is correct and example exists, and not yet shown
                    if st.session_state.selected_mcq_choice == mcq["answer"] and st.session_state.cached_real_life_example and not st.session_state.show_real_life_example_section:
                        if st.button("🌍 Show Real-Life Example", key="show_real_life_example_btn_after_quiz"): # Unique key
                            st.session_state.show_real_life_example_section = True
                            st.rerun() # Rerun to display the real-life example section

                st.markdown(f'</div>', unsafe_allow_html=True) # Close the mcq-display-box div


            # ——— Conditionally display Real-Life Example Section ———
            # This section is now displayed only if its flag is True AND the example content exists
            if st.session_state.show_real_life_example_section and st.session_state.cached_real_life_example:
                st.markdown("---")
                st.markdown("### 🌍 Real-Life Example!")
                st.markdown(f'<div class="real-life-example-box">💡 {st.session_state.cached_real_life_example}</div>', unsafe_allow_html=True)
                
                # After real-life example is shown, display "Show Related Topics" button
                # This is the only place "Show Related Topics" button should appear IF quiz and RLE were part of the flow.
                if st.session_state.related and not st.session_state.show_related_topics_section and not st.session_state.related_topic_answer:
                    if st.button("📚 Show Related Topics", key="show_related_topics_after_rle_btn"):
                        st.session_state.show_related_topics_section = True
                        st.rerun()
            
            # If quiz was shown, but no real-life example was generated (e.g., incorrect answer or API failure for RLE)
            # then show "Show Related Topics" button after quiz feedback.
            elif st.session_state.show_quiz_section and st.session_state.mcq and \
                 st.session_state.feedback and \
                 (st.session_state.selected_mcq_choice != st.session_state.mcq["answer"] or st.session_state.cached_real_life_example is None) and \
                 st.session_state.related and not st.session_state.show_related_topics_section and \
                 not st.session_state.related_topic_answer:
                if st.button("📚 Show Related Topics", key="show_related_topics_after_quiz_feedback_btn"): # Changed key
                    st.session_state.show_related_topics_section = True
                    st.rerun()


            # ——— Related Topics Section (Conditionally displayed) ———
            if st.session_state.show_related_topics_section and st.session_state.related:
                st.markdown("#### Related Topics")
                # Use st.columns for horizontal layout of related topic buttons
                # Create columns dynamically based on the number of related topics, up to a max of 3 for good spacing
                num_r_cols = min(len(st.session_state.related), 3)
                rcols = st.columns(num_r_cols)
                for i, rt_text in enumerate(st.session_state.related): # Iterate over related topics text directly
                    # When a related topic button is clicked
                    with rcols[i % num_r_cols]: # Distribute buttons across columns
                        if st.button(rt_text, key=f"rel_{i}"): 
                            # IMPORTANT: Do NOT change st.session_state.question, answer, mcq here
                            # These should remain for the *original* question.
                            
                            with st.spinner(f"Getting answer for '{rt_text}'..."):
                                # Get AI answer for the related topic and store in a *separate* state variable
                                st.session_state.related_topic_answer = get_ai_answer(rt_text, grade, subject, api_key)
                            
                            # Reset feedback for the main MCQ, as context might have shifted
                            st.session_state.feedback = None 
                            st.session_state.selected_mcq_choice = None # Clear selected MCQ choice when related topic is clicked
                            st.session_state.show_quiz_section = False # Hide quiz when related topic is clicked
                            st.session_state.show_real_life_example_section = False # Hide real-life example when related topic is clicked
                            st.session_state.cached_real_life_example = None # Clear cached example
                            st.session_state.show_related_topics_section = False # Hide related topics section after clicking one
                            st.rerun() # Rerun to display related answer

        # ——— Related Answers Box (New Section, at the very end of the main display logic) ———
        if st.session_state.related_topic_answer:
            st.markdown("---") # Separator
            # Changed caption to "📚 Related Topic Answer"
            st.markdown("### 📚 Related Topic Answer")
            # Added an emoji prefix to the related answer box for attractiveness
            st.markdown(f'<div class="related-answer-box">✨ {st.session_state.related_topic_answer}</div>', unsafe_allow_html=True)

            # --- Navigation Buttons (Conditional Display) ———
            # Buttons now show ONLY if related_topic_answer is present
            st.markdown("---") # Separator before navigation buttons
            col_next, col_exit = st.columns(2)

            with col_next:
                if st.button("➡️ New Question", key="next_question_btn"):
                    # Clear all relevant states to start fresh
                    st.session_state.question = ""
                    st.session_state.answer = ""
                    st.session_state.related = None
                    st.session_state.mcq = None
                    st.session_state.feedback = None
                    st.session_state.related_topic_answer = None
                    st.session_state.selected_mcq_choice = None
                    st.session_state.show_sample_questions = True # Show samples again
                    st.session_state.show_quiz_section = False # Reset quiz visibility
                    st.session_state.show_real_life_example_section = False # Reset real-life example visibility
                    st.session_state.cached_real_life_example = None # Clear cached example
                    st.session_state.show_related_topics_section = False # Reset related topics visibility
                    st.session_state.show_sample_questions_buttons = False # Hide sample questions buttons
                    st.rerun() # Force a rerun to clear and display initial state

            with col_exit:
                if st.button("❌ Exit App", key="exit_app_btn"):
                    # Clear session state to ensure a clean start on the main page
                    st.session_state.clear()
                    # Use st.switch_page to go back to the main app.py
                    # Changed from "2_AI_Learning_Mode" back to "app"
                    st.switch_page("app.py")

    else:
        # Welcome message when no grade/subject is selected
        st.info("👋 Welcome! Please select both a grade and a subject from the dropdowns above to begin your learning journey!")
