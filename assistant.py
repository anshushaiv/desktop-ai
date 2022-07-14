import speech_recognition as sr
import pyttsx3

from time import sleep
from datetime import datetime
import webbrowser
import os.path as path
import ast

class Assistant:
    """This class contains information about the 'personality' the assistant should have"""
    name = "Jarvis"
    master = " "

    r = sr.Recognizer()
    engine = pyttsx3.init()

    voice_properties = dict()
    misc_properties = {"name": name, "master": master}

    def __init__(self, name = "Jarvis", master = ' '):
        self.name = name
        self.master = master

    def update_misc_properties(self):
        self.name = self.misc_properties["name"]
        self.master = self.misc_properties["master"]

    def load_misc_properties(self):
        fn = "misc_properties"
        if path.isfile(fn):
            file = open(fn, 'r')
            contents = file.read()
            self.misc_properties = ast.literal_eval(contents)
            file.close()
        else:
            file = open(fn, 'w')
            file.write(str(self.misc_properties))
            file.close
        self.update_misc_properties()

    def save_misc_properties(self):
        fn = "misc_properties"
        file = open(fn, 'w')
        file.write(str(self.misc_properties))
        file.close()

    def load_voice_properties(self):
        fn = "voice_properties"
        if path.isfile(fn):
            file = open(fn, "r")
            contents = file.read()
            self.voice_properties = ast.literal_eval(contents)
            file.close()

            # setting voice engine properties
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[self.voice_properties['voice']])
            self.engine.setProperty('rate', self.voice_properties['rate'])
            self.engine.setProperty('volume', self.voice_properties['volume'])
        else:
            # create file with default settings
            self.voice_properties['voice'] = 0
            self.voice_properties['rate'] = self.engine.getProperty('rate')
            self.voice_properties['volume'] = self.engine.getProperty('volume')
            file = open(fn, "w")
            file.write(str(self.voice_properties))

    def save_voice_properties(self):
        fn = "voice_properties"
        file = open(fn, 'w')
        file.write(str(self.voice_properties))
        file.close()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def recognize_voice(self):
        text = ''
        # use standard microphone as source
        with sr.Microphone() as source:
            # adjust for ambient noise
            self.r.adjust_for_ambient_noise(source)
            # capture voice
            voice = self.r.listen(source)

            try:
                text = self.r.recognize_google(voice)
            except sr.RequestError:
                self.speak("Sorry, I cannot connect to the API...")
            except sr.UnknownValueError:
                self.speak("Sorry, I did not catch that...")
            
            return text.lower()

    def say_name(self):
        self.speak("My name is " + self.name)
        return True

    def say_date(self):
        date = datetime.now().strftime("%d %m %Y")
        self.speak("Today is " + date)
        return True

    def say_time(self):
        time = datetime.now().time().strftime("%H %M").split()
        time_as_ints = [int(time[0]), int(time[1])]
        time_suffix = ''
        if time_as_ints[0] > 12:
            time_suffix = 'p.m.'
            time_as_ints[0] = time_as_ints[0] - 12
        else:
            time_suffix = 'a.m.'
        time = str(time_as_ints[0])+ ' ' + str(time_as_ints[1]) + ' ' + time_suffix
        self.speak("It is " + time)
        return True

    def search(self):
        self.speak('What would you like me to search')
        keywords = self.recognize_voice()
        if keywords != '':
            url = 'https://www.google.com/search?q=' + keywords
            self.speak('Here are the results for ' + keywords)
            webbrowser.open(url)
            return True

    def quit(self):
        self.speak('Goodbye...')
        return False

    def unrecognized(self):
        self.speak('Sorry, I did not understand that')
        return True

    def status_report(self):
        time = self.say_time()
        self.speak('on the')
        date = self.say_date()
        return time and date

    def reply(self, text):
        if "name" in text:
            return self.say_name()
        elif "date" in text:
            return self.say_date()
        elif "time" in text:
            return self.say_time()
        elif "search" in text:
            return self.search()
        elif "status" in text and "report" in text:
            return self.status_report()
        elif "quit" in text or "exit" in text:
            return self.quit()
        else:
            return self.unrecognized()

    def greet(self):
        time = datetime.now().time().strftime("%H %M")
        hour = int(time.split()[0])
        time_of_day = ''
        if (hour < 12):
            time_of_day = "good morning"
        elif (hour < 18):
            time_of_day = "hello"
        else:
            time_of_day = "good evening"

        greeting_fst = time_of_day + " " + self.master
        self.speak(greeting_fst)

        greeting_snd = self.name + " is now ready to assist you"
        self.speak(greeting_snd)

    def assist(self):
        self.greet()
        sleep(1)
        cont = True
        while cont:
            voice = self.recognize_voice()
            words = voice.split()
            if len(words) > 0:
                if words[0] == self.name:
                    if len(words) > 1:
                        cont = self.reply(words[1:])
                    else:
                        self.speak('Sorry, I did not understand that')
