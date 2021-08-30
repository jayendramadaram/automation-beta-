import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia 
import os
import smtplib
import sqlite3
from selenium import webdriver
from playsound import playsound
import random
import requests
from bs4 import BeautifulSoup
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("yo buddy i am triffiny an artificial intelligence bot automated by jay")  
    speak('So as you are thinking to use me do already have a account or wanna setup new')     

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")  
        return ""
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('recpanther@gmail.com', 'Iamaking8')
    server.sendmail('recpanther@gmail.com', to, content)
    server.close()

def login():
    speak('oh cool whats your user name')
    un = takeCommand().lower()
    while un == "":
        speak("username again")
        un = takeCommand().lower()
    speak('and whats your password')
    pw = takeCommand().lower()
    while pw == "":
        speak("password again")
        pw = takeCommand().lower()
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT pw FROM users WHERE name=?' , (un.lower(),))
    pwf = cursorObj.fetchall()
    con.commit()
    print(pwf)
    if pwf!=[] and pw.lower() == pwf[0][0].lower():
        speak('congrats bud keep going')
        return True
    else:
        speak('i guess your credentials didnt match trying singing in or logging again')

def signup():
    speak('chalo lets create your account whats your username')
    un = takeCommand().lower()
    while un =="":
        speak("please a bit clear")
        un = takeCommand().lower()
    speak('and whats your password')
    pw = takeCommand().lower()
    while pw=="":
        speak("please a bit clear")
        pw = takeCommand().lower()
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    entities = (un , pw)
    cursorObj.execute('INSERT INTO users(name, pw) VALUES(?, ?)', entities)
    con.commit()
    speak('yayyy successfully created')
    return

def loggs():
    speak('speak up')
    logg = takeCommand().lower()
    while logg=="":
        speak("please a bit clear")
        logg = takeCommand().lower()
    if 'have' in logg or 'already' in logg or 'login' in logg:
        if login():
            return
        else:
            loggs()
    elif 'create' in logg or 'signin' in logg:
        signup()
        return
    elif 'quit' in logg:
        speak('signing off')
        quit()
    else:
        speak('sorry dude i didnt get you could you be a bit clear')
        loggs()

if __name__ == "__main__":
    wishMe()
    loggs()
    speak('enterring while loop')
    # speak('le me show you what can i do for ya')
    # speak(' i can send mails open ,youtube and play vedios,play the music , search on google and wikipedia and tons of stuff')
    while True:
        query = takeCommand().lower()
        while query =="":
            # speak("please a bit clear")
            query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif query.lower().startswith('open'):
            
            if query.lower().endswith('youtube'):
                run = webdriver.Chrome("C:\webdrivers\chromedriver.exe")
                speak('openning requirements on YT')
                st = ''.join(query.strip().split()[1:-1])
                run.get('https://www.youtube.com/results?search_query={}'.format(st))
                time.sleep(3)
                logy = run.find_element_by_xpath('//*[@id="thumbnail"]').click()
            
            
        elif 'quit' in query and 'youtube' in query:
            try:run.quit()
            except:continue

        elif query.lower().startswith('play'):
            path = r"C:\Users\jayendra\Music"
            yo = random.choice(os.listdir(path))
            hey=  'C:/Users/jayendra/Music/' + yo
            playsound(hey)
            
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                while content == "":
                    content = takeCommand()
                speak("whom shall i mail it")
                to = takeCommand()
                while to == "":
                    to = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend  I am not able to send this email")

        elif query.startswith("what") or query.startswith("how")  or query.startswith("when")  or query.startswith("where")  or query.startswith("who")  or query.startswith("name")  or query.startswith("is") :
            URL = "https://www.google.co.in/search?q=" + query
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
                }
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                result = soup.find(class_='Z0LcW XcVN5d').get_text()
                speak(result)
            except:speak('lets try again')
        else:
            URL = "https://www.google.co.in/search?q=" + query
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
                }
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                result = soup.find(class_='Z0LcW XcVN5d').get_text()
                speak(result)
            except:speak('lets try again')
            
            

