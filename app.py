
import os
import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv
import threading
import queue

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)

# Set up Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[])

# Initialize queue for TTS
tts_queue = queue.Queue()

# Background thread to handle all TTS safely
def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        engine.say(text)
        try:
            engine.runAndWait()
        except RuntimeError:
            pass
        tts_queue.task_done()

# Start TTS thread (run once when app starts)
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

# Use this to speak safely
def speak_text(text):
    tts_queue.put(text)

def get_gemini_response(user_input):
    convo.send_message(user_input)
    return convo.last.text

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I didn't catch that.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition.")
    return ""

# Streamlit UI
st.set_page_config(page_title="Gemini Voice Assistant", layout="centered")
st.title("🎙️ Gemini Voice Assistant")

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "gemini_reply" not in st.session_state:
    st.session_state.gemini_reply = ""

# Button to start speech recognition
if st.button("🎧 Start Speaking"):
    user_input = recognize_speech()
    if user_input:
        st.session_state.user_input = user_input  # Store the input for editing
        st.success(f"**You said:** {user_input}")

# Text Input to edit recognized speech
user_input = st.text_area("Edit Recognized Speech", value=st.session_state.user_input, height=100)

# Generate Response Button
if st.button("Generate Response"):
    if user_input:
        gemini_response = get_gemini_response(user_input)
        st.session_state.gemini_reply = gemini_response
        st.write("🤖 Gemini says:", gemini_response)
        speak_text(gemini_response)

# Display the transcript and response
st.text_area("🎤 Transcribed Input", st.session_state.user_input, height=100)
st.text_area("🤖 Gemini Response", st.session_state.gemini_reply, height=150)
