import threading
import time
import speech_recognition as sr
from voice import speak_worker, speak, speak_queue 
from recognizer import callback
from browser import driver

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)

    threading.Thread(target=speak_worker, daemon=True).start()

    stop_listening = r.listen_in_background(mic, callback)

    speak("Добрый день, сэр")
    speak("Говорите, я вас слушаю")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Завершение работы...")
        stop_listening()           
        speak_queue.put(None)    
        if driver:
            driver.quit()
