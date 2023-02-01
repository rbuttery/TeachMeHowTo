import streamlit as st
import os
import openai

# OpenAI API key setup
openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(page_title="Teach me how to...", page_icon="🤖")

# Function to generate response from OpenAI's Completion API
# Cache the result to avoid repetitive calculations
@st.cache
def ask(prompt):
    # Set up the parameters for the API request
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n###\n"],
    )
    # Extract the answer from the response
    answer = response['choices'][0]['text'].replace('\n\n', '')
    return answer

# Function to add a variable to Streamlit's session state
def add_variable(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

# Function to update a variable in Streamlit's session state
def update_variable(key, value):
    st.session_state[key] = value

# Function to retrieve a variable from Streamlit's session state
def get_variable(key):
    return st.session_state[key]

# Page title
st.title("Teach me how to...")

# Text input for the user's request
TEACH_ME_HOW_TO = st.text_input("", placeholder="Take over the world...")

# If the user has entered a request
if TEACH_ME_HOW_TO:
    # Construct the prompt for OpenAI's Completion API
    PROMPT_TEXT = f""" You are the world's best teacher. You can teach someone a complex topic in only a few sentences. With an Intro, list of steps & in as few words as possible, teach me how to {TEACH_ME_HOW_TO}. """
    if PROMPT_TEXT:
        # Generate the response from OpenAI
        AI_RESPONSE = ask(
            f"""{PROMPT_TEXT} RETURN THIS DOCUMENT AS HTML with headers, lists, and formatting""")
        # Update the AI response in the session state
        update_variable("AI_RESPONSE", AI_RESPONSE)
        st.markdown(AI_RESPONSE, unsafe_allow_html=True)

# Try to display the AI response if it exists in the session state
try:
    num_steps = ask(f'How many steps are there here? please return only an integer. {get_variable("AI_RESPONSE")}')

    for i in range(int(num_steps)):
        
        step = ask(f'Identify step {i+1} from this guide. Give a 2 minute explanation in great detail, give examples make it relavent to anyone trying to learn: {get_variable("AI_RESPONSE")}')
        
        st.markdown(f"### Step {i+1}")
        st.markdown(
            step, unsafe_allow_html=True)
        
        # add_variable(f"step_{i+1}", step)
except KeyError:
    pass
