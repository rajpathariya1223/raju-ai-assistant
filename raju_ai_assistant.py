import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
import os
import datetime

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# OpenAI API Key (Replace with your key)
openai.api_key = "write your api key here "

# Function to make Raju speak
def speak(text):
    print(f"Raju: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen and convert voice to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except Exception as e:
        speak("Sorry, I didn't catch that.")
        return ""

# Memory (can be extended)
memory = {}

# Wake word system
def activated(command):
    return "raju" in command

# Command Processing Logic
def process_command(command):
    command = command.replace("raju", "").strip()

    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "remember" in command:
        item = command.replace("remember", "").strip()
        memory["note"] = item
        speak(f"I will remember: {item}")

    elif "what did you remember" in command:
        note = memory.get("note", "I don't remember anything yet.")
        speak(note)

    else:
        speak("Let me think...")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=command,
            max_tokens=100
        )
        reply = response.choices[0].text.strip()
        speak(reply)

# Main loop
def main():
    speak("Hello, I'm Raju, your assistant.")
    while True:
        command = listen()
        if activated(command):
            if "stop listening" in command:
                speak("Okay, I’ll wait for your next command.")
                break
            process_command(command)

if __name__ == "__main__":
    main()
