# import os
# import streamlit as st
# import speech_recognition as sr
# import pyttsx3
# import google.generativeai as genai
# from dotenv import load_dotenv
# import threading

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Set up Gemini model
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 0,
#     "max_output_tokens": 8192,
# }
# safety_settings = [
#     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
# ]

# model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)
# convo = model.start_chat(history=[])

# # Text-to-speech setup
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
# engine.setProperty('rate', 200)

# def get_gemini_response(user_input):
#     convo.send_message(user_input)
#     return convo.last.text

# def speak_text(text):
#     def run():
#         engine.say(text)
#         engine.runAndWait()
#     threading.Thread(target=run).start()

# def recognize_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("🎤 Listening...")
#         audio = recognizer.listen(source, timeout=5)
#         try:
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.UnknownValueError:
#             st.error("Sorry, I didn't catch that.")
#         except sr.RequestError:
#             st.error("Could not request results from Google Speech Recognition.")
#     return ""

# # Streamlit UI
# st.set_page_config(page_title="Gemini Voice Assistant", layout="centered")
# st.title("🎙️ Gemini Voice Assistant")

# if st.button("🎧 Start Speaking"):
#     user_input = recognize_speech()
#     if user_input:
#         st.success(f"**You said:** {user_input}")
#         gemini_response = get_gemini_response(user_input)
#         st.write("🤖 Gemini says:", gemini_response)
#         speak_text(gemini_response)

# if "transcript" not in st.session_state:
#     st.session_state.transcript = ""
# if "gemini_reply" not in st.session_state:
#     st.session_state.gemini_reply = ""

# if st.button("🎧 Listen"):
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Listening... Speak now.")
#         try:
#             audio = recognizer.listen(source, timeout=5.0)
#             user_text = recognizer.recognize_google(audio)
#             st.session_state.transcript = user_text
#             st.success(f"You said: {user_text}")

#             response = get_gemini_response(user_text)
#             st.session_state.gemini_reply = response
#             st.success(f"Gemini says: {response}")

#             speak_text(response)

#         except sr.UnknownValueError:
#             st.error("Sorry, I couldn't understand.")
#         except sr.WaitTimeoutError:
#             st.error("Listening timed out.")
#         except Exception as e:
#             st.error(f"Error: {str(e)}")

# st.text_area("🎤 Transcribed Input", st.session_state.transcript, height=100)
# st.text_area("🤖 Gemini Response", st.session_state.gemini_reply, height=150)


# Updated app.py
# import os
# import streamlit as st
# import speech_recognition as sr
# import pyttsx3
# import google.generativeai as genai
# from dotenv import load_dotenv
# import threading
# import requests
# from bs4 import BeautifulSoup

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Set up Gemini model
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 0,
#     "max_output_tokens": 8192,
# }
# safety_settings = [
#     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
# ]

# model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)
# convo = model.start_chat(history=[])

# # Text-to-speech setup
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
# engine.setProperty('rate', 200)

# def get_gemini_response(user_input):
#     if "sena" in user_input.lower():
#         return fetch_sena_info()
#     convo.send_message(user_input)
#     return convo.last.text


# def speak_text(text):
#     def run():
#         try:
#             engine.say(text)
#             engine.runAndWait()
#         except RuntimeError as e:
#             if "run loop already started" in str(e):
#                 engine.endLoop()
#                 engine.say(text)
#                 engine.runAndWait()
#     threading.Thread(target=run).start()



# def recognize_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("🎤 Listening...")
#         audio = recognizer.listen(source, timeout=5)
#         try:
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.UnknownValueError:
#             st.error("Sorry, I didn't catch that.")
#         except sr.RequestError:
#             st.error("Could not request results from Google Speech Recognition.")
#     return ""

# import requests
# from bs4 import BeautifulSoup

# def fetch_sena_info():
#     try:
#         response = requests.get("https://sena.services")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         text = " ".join([p.get_text(strip=True) for p in paragraphs])
#         return text if text else "Sena website does not contain enough information."
#     except Exception as e:
#         return f"Error fetching Sena info: {e}"


# def fetch_cricket_results():
#     try:
#         response = requests.get("https://www.espncricinfo.com/live-cricket-score")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         matches = soup.find_all('div', class_='ds-text-tight-s')
#         if matches:
#             return matches[0].get_text(strip=True)
#         return "Couldn't find cricket match results."
#     except Exception as e:
#         return f"Error fetching cricket results: {e}"

# # Streamlit UI
# st.set_page_config(page_title="Gemini Voice Assistant", layout="centered")
# st.title("🎙️ Gemini Voice Assistant")

# if "transcript" not in st.session_state:
#     st.session_state.transcript = ""
# if "gemini_reply" not in st.session_state:
#     st.session_state.gemini_reply = ""

# if st.button("🎧 Start Speaking"):
#     user_input = recognize_speech().lower()
#     if user_input:
#         st.success(f"**You said:** {user_input}")

#         if "sena" in user_input:
#             gemini_response = fetch_sena_info()
#         elif "cricket" in user_input or "match result" in user_input:
#             gemini_response = fetch_cricket_results()
#         else:
#             gemini_response = get_gemini_response(user_input)

#         st.write("🤖 Gemini says:", gemini_response)
#         speak_text(gemini_response)
#         st.session_state.transcript = user_input
#         st.session_state.gemini_reply = gemini_response

# st.text_area("🎤 Transcribed Input", st.session_state.transcript, height=100)
# st.text_area("🤖 Gemini Response", st.session_state.gemini_reply, height=150)

# # Updated requirements.txt file
# # streamlit
# # SpeechRecognition
# # pyttsx3
# # google-generativeai
# # python-dotenv
# # pyaudio
# # requests
# # beautifulsoup4


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
