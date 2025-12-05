import threading
import time
from app.voice import start_speak_worker, speak, stop_speak_worker
from app.recognizer import start_recognizer_background, start_console_worker
from app.browser import driver

def main():
    start_speak_worker()
    stop_listening = start_recognizer_background()
    start_console_worker()

    speak("Бот включён")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Завершение работы...")
        if stop_listening:
            try:
                stop_listening(wait_for_stop=False)
            except:
                pass
        stop_speak_worker()
        try:
            if driver:
                driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()
