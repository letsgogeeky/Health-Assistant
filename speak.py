from gtts import gTTS
import os


def speak_words(words):
    tts = gTTS(text=words, lang='en')
    print(words)
    tts.save("result_speech.mp3")
    os.system("mpg321 result_speech.mp3")