import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from email.message import EmailMessage

class PersonalAssistant:
    def __init__(self):
        # Initialize pyttsx3
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.recognizer = sr.Recognizer()
        self.email_credentials = {
            'email': 'lokeshbharambe26@gmail.com',
            'password': 'Lokesh@4426'
        }

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def wish_me(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am your personal assistant. Please tell me how may I help you")

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Could not understand audio, please say that again...")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        return query.lower()

    def send_email(self, to, subject, content):
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self.email_credentials['email']
        msg['To'] = to

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_credentials['email'], self.email_credentials['password'])
            server.send_message(msg)
            server.quit()
            self.speak("Email has been sent!")
        except Exception as e:
            print(e)
            self.speak("Sorry, I am not able to send this email")

    def execute_query(self, query):
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'open visual code' in query:
            vscode_path = r'C:\Users\hp\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            if os.path.isfile(vscode_path):
                os.startfile(vscode_path)
            else:
                self.speak("Visual Studio Code not found.")
        elif 'open edge' in query:
            edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
            if os.path.isfile(edge_path):
                os.startfile(edge_path)
            else:
                self.speak("Microsoft Edge not found.")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"Sir, the time is {strTime}")
        elif "exit" in query:
            self.speak("Goodbye!")
            exit()
        elif 'email to harry' in query:
            self.speak("What should I say?")
            content = self.take_command()
            if content:
                self.send_email("harry@example.com", "Message from your assistant", content)
            else:
                self.speak("Sorry, I couldn't get your message.")
        else:
            self.speak("I am sorry, I don't have a response for that query.")

if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.wish_me()
    while True:
        query = assistant.take_command()
        if query:
            assistant.execute_query(query)
