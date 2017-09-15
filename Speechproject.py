import speech_recognition as sr
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import style

style.use('fivethirtyeight')

RATE = 4410
CHUNK = int(RATE/20) # RATE / number of updates per second

def soundplot(stream):
    t1=time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    plt.plot(data)
    plt.title(i)
    plt.xlabel("Sound data")
    plt.grid()
    plt.axis([0,len(data),-2**16/2,2**16/2])
    plt.savefig("03.png",dpi=50)
    plt.close("all")
if __name__=="__main__":
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    if stream == 0:
        print("No input")
    for i in range(10):
        soundplot(stream)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("You said: " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #do this for 10 seconds

    stream.stop_stream()
    stream.close()
    p.terminate()


