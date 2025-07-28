# Project Context for AI Learning Companion Streamlit

## Overview
This project is an AI-powered learning companion built with Streamlit.
Its primary purpose is to provide an interactive educational experience, including:
- AI-generated content (e.g., explanations, summaries)
- Interactive quizzes (MCQs)
- Different learning modes (e.g., student mode, AI learning mode, chatbot modes for grades).

## Key Technologies
- **Frontend/Framework:** Streamlit (Python)
- **AI Model:** Google Gemini API
- **Language:** Python

## Code Style Guidelines
- Follow PEP 8 for Python code.
- Use clear and descriptive variable/function names.
- Prefer f-strings for string formatting.
- Add comments for complex logic or non-obvious parts of the code.

## Application Structure
- `app.py`: Main entry point for the Streamlit application.
- `pages/`: Contains separate Streamlit pages for different functionalities (e.g., student mode, learning mode, grade-specific chatbots).
- `assets/`: Stores static assets like images.
- `.venv/`: Virtual environment for project dependencies.

## Important Notes for AI
- When generating Streamlit code, use `streamlit` (imported as `st`) functions.
- For MCQ sections, ensure the structure uses `st.radio` for choices and manages state with `st.session_state`.
- Pay attention to session state management for persistent data across reruns.
- The `unsafe_allow_html=True` flag is used for custom styling in markdown; be mindful of security implications if widely used.

---
**Your instructions to Gemini go here. For example:**

"When I ask for a new Streamlit feature, try to provide a complete code block that can be directly added to a `.py` file within the `pages/` directory."

"If I ask to refactor code, prioritize making it more modular and readable, especially for Streamlit components."

"When I inquire about a specific grade's chatbot, refer to the corresponding file in `pages/` (e.g., `Grade_4_chatbot.py`)."