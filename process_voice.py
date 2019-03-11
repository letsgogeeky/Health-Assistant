import speech_recognition as sr
import os

#We use here SpeechRecognition library to transform voice into text that we can process
# to form the medical diagnosis
def GetTextFromSpeechUsingGoogle():
    rec = sr.Recognizer()
    with sr.Microphone() as result:
        print("listening now...!")
        #The following line is a function that tries to filter out noise
        #  in the room to get the actual words.
        rec.adjust_for_ambient_noise(result, duration=0.5)
        #The following line saves what's been said in the microphone in an audio object.
        audio = rec.listen(result)

        #The recognize_google function sends the audio object obtained earlier to google to
        # turn it into text and return it to the main program to start processing it.
    return rec.recognize_google(audio, language="en-GB")