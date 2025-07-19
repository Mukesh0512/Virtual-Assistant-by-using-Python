import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your NewsAPI Key>"  # Optional: add your newsapi.org key here

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c:
        if not newsapi or "<" in newsapi:
            speak("Please add your News API key in the code.")
            return
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
    else:
        speak("Sorry, I cannot process that request.")

# Optional: CLI entrypoint
if __name__ == "__main__":
    speak("Jarvis initialized.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error:", e)



