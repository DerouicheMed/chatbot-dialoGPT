import speech_recognition as sr
import winsound
import pyttsx3
import json
import requests
from params import HF_API_TOKEN

## Hugging Face API url. the chatbox model url we are using
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}


## init text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)
engine.setProperty('rate', 165)

## define speak function
def speak(text):
    print('>> Computer: ' + text)
    engine.say(text)
    engine.runAndWait()


r = sr.Recognizer()                                                                                   
with sr.Microphone() as source:  

    speak('Speak after the bip')
    ## generate beep sound to indicade to user when to speak
    winsound.Beep(500,150)   

    ## try listening to microphone and transcribing speech
    try:
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
        query = r.recognize_google(audio)
        print('>> User: ' + query)
    except:
        print('!! exception while listening to command')
        speak("Sorry sir I can't hear you correctly.")
        query=''


data = {
    "inputs": {
        "generated_responses": [],
        "past_user_inputs": [],
        "text": query.lower()
    }
  }

response = requests.request("POST", API_URL, headers=headers, data=data)
response = json.loads(response.content.decode("utf-8"))
print(response)
response =  response['generated_text'].lower()
speak(response)
    