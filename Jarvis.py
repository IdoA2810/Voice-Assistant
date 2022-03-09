import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

from JarvisSpotify import *


def initalize_spotify():
    auth_manager = SpotifyOAuth(client_id = "21d4c17e287f4da19981024d5600e457",
                                client_secret = "e55fd58cac6b4baf807ba84d0772b52a",
                                redirect_uri = "https://example.com/callback/",
                                scope = "user-read-private user-read-playback-state user-modify-playback-state",
                                username = "w5f2ieytlrcz4u7v08boqqijd")
    spotify = sp.Spotify(auth_manager=auth_manager)
    return spotify

def get_device_id(spotify):
    device_name = "laptop-lvpifu49"
    devices = spotify.devices()

    for d in devices['devices']:
        if d['name'] == device_name:
            return d['id']



def main():

    spotify = initalize_spotify()
    deviceID = get_device_id(spotify)

    running = True
    r = sr.Recognizer()
    engine = pyttsx3.init()

    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[3].id)
    engine.setProperty('rate', 150) #default is 200

    while running:
        with sr.Microphone() as source:
            #print("Say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                text = r.recognize_google(audio)
                print("Jarvis thinks you said " + text)
                text = text.lower()

                if text.split(" ")[0] == "jarvis":
                    if len(text.split(" ")) == 1:
                        engine.say("How can i help?")
                        engine.runAndWait()
                        audio = r.listen(source)
                        text += " " + r.recognize_google(audio)

                    text = text.split(" ", 1)[1]

                    if text.split(" ")[0] == "play":
                        if len(text.split(" ")) == 1:
                            engine.say("Which song, album, or artist would you like me to play?")
                            engine.runAndWait()
                            audio = r.listen(source)
                            text += " " + r.recognize_google(audio)

                        text = text.split(" ", 1)[1]
                        try:
                            if text.split(" ")[0] == 'album':
                                text = text.split(" ", 1)[1]
                                uri = get_album_uri(spotify=spotify, name=text)
                                engine.say("Playing " + text)
                                engine.runAndWait()
                                play_album(spotify=spotify,device_id=deviceID, uri=uri)
                            elif text.split(" ")[0] == 'artist':
                                text = text.split(" ", 1)[1]
                                uri = get_artist_uri(spotify=spotify, name=text)
                                engine.say("Playing " + text)
                                engine.runAndWait()
                                play_artist(spotify=spotify,device_id=deviceID, uri=uri)
                            else:
                                uri = get_track_uri(spotify=spotify, name=text)
                                engine.say("Playing " + text)
                                engine.runAndWait()
                                play_track(spotify=spotify,device_id=deviceID, uri=uri)
                        except InvalidSearchError:
                            engine.say("I couldn't find what you were looking for.")
                            engine.runAndWait()

                    elif text == "who are you" or text == "what's your name" or text == "what is your name":
                        engine.say("my name is Jarvis!")
                        engine.runAndWait()

                    elif text == "hello":
                        engine.say("Hello sir")
                        engine.runAndWait()

                    elif text == "exit" or text == "goodbye":
                        engine.say("Goodbye")
                        engine.runAndWait()
                        running = False

                    elif text.split(" ")[0] == "start":

                        if len(text.split(" ")) == 1:
                            engine.say("Which app would you like me to start?")
                            engine.runAndWait()
                            print("Say something!")
                            audio = r.listen(source)
                            text += " " + r.recognize_google(audio)
                        try:
                            os.startfile(" ".join(text.split(" ")[1:]) + ".exe")
                            engine.say("Starting " + " ".join(text.split(" ")[1:]))
                            engine.runAndWait()
                        except FileNotFoundError:
                            engine.say("I couldn't find the app you were looking for")
                            engine.runAndWait()

                    elif text.split(" ")[0] == "open":
                        if len(text.split(" ")) == 1:
                            engine.say("Which site would you like me to open?")
                            engine.runAndWait()
                            print("Say something!")
                            audio = r.listen(source)
                            text += " " + r.recognize_google(audio)
                        engine.say("Opening " + " ".join(text.split(" ")[1:]))
                        engine.runAndWait()
                        webbrowser.open("http://" + " ".join(text.split(" ")[1:]) + ".com")

                    elif text.split(" ")[0] == "youtube":
                        if len(text.split(" ")) == 1:
                            engine.say("Which song or video would you like me to play?")
                            engine.runAndWait()
                            print("Say something!")
                            audio = r.listen(source)
                            text += " " + r.recognize_google(audio)
                        engine.say("Playing " + " ".join(text.split(" ")[1:]))
                        engine.runAndWait()
                        pywhatkit.playonyt(" ".join(text.split(" ")[1:]))

                    elif text.split(" ")[0] == "search":
                        if len(text.split(" ")) == 1:
                            engine.say("What would you like me to search?")
                            engine.runAndWait()
                            print("Say something!")
                            audio = r.listen(source)
                            text += " " + r.recognize_google(audio)
                        engine.say("Searching " + " ".join(text.split(" ")[1:]))
                        engine.runAndWait()
                        pywhatkit.search(" ".join(text.split(" ")[1:]))

                    elif text == "semi":
                        engine.say("I'm Semi I stay automatic")
                        engine.say("Money add then multiply")
                        engine.say("I call that mathe-mat-a-matics")
                        engine.runAndWait()
                        webbrowser.open("https://www.youtube.com/watch?v=VFVK1cd9P2k")

                    elif text == "dc":
                        engine.say("Opening DC Universe Online Bot")
                        engine.runAndWait()
                        os.startfile("D:\Projects\DCUO Automation\Bot1.py")

            except sr.UnknownValueError:
                #print("Google Speech Recognition could not understand audio")
                pass

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    main()