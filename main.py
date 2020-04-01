import speech_recognition as sr

if __name__ == '__main__':
    r = sr.Recognizer()
    harvard = sr.AudioFile('./data/OSR_us_000_0010_8k.wav')
    with harvard as source:
        audio = r.record(source)
        google_text = r.recognize_google(audio)
        sphinx_text = r.recognize_sphinx(audio)
        print(google_text)
        print(sphinx_text)
