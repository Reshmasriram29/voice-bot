
# Updated voice.py
import os
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize pyttsx3
listening = True
sending_to_gemini = False
engine = pyttsx3.init()

# Set up the model
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

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[])

def get_response(user_input):
    convo.send_message(user_input)
    gemini_reply = convo.last.text
    print("Gemini:", gemini_reply)
    return gemini_reply

def fetch_sena_info():
    try:
        response = requests.get("https://sena.services")
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text(strip=True) for p in paragraphs])
        return text if text else "Sena website does not contain enough information."
    except Exception as e:
        return f"Error fetching Sena info: {e}"

def fetch_cricket_results():
    try:
        response = requests.get("https://www.espncricinfo.com/live-cricket-score")
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.find_all('div', class_='ds-text-tight-s')
        if matches:
            return matches[0].get_text(strip=True)
        return "Couldn't find cricket match results."
    except Exception as e:
        return f"Error fetching cricket results: {e}"

exit_words = ["exit", "stop", "quit", "bye", "goodbye"]
wake_word = "gemini"

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            response = recognizer.recognize_google(audio)
            print("You said:", response)

            if any(exit_word in response.lower() for exit_word in exit_words):
                sending_to_gemini = False
                print("Stopped sending responses to Gemini.")
                continue

            if wake_word in response.lower() and not sending_to_gemini:
                sending_to_gemini = True
                print("Resumed sending responses to Gemini.")

            if sending_to_gemini:
                lower_response = response.lower()
                if "sena" in lower_response:
                    reply = fetch_sena_info()
                elif "cricket" in lower_response or "match result" in lower_response:
                    reply = fetch_cricket_results()
                else:
                    reply = get_response(response)
                engine.setProperty('rate', 200)
                engine.setProperty('volume', volume)
                engine.setProperty('voice', voices[0].id)
                engine.say(reply)
                engine.runAndWait()

        except sr.UnknownValueError:
            print("Didn't recognize anything.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except Exception as e:
            print("Error:", str(e))
