import queue
import pythoncom
import win32com.client

speak_queue = queue.Queue()

def speak_worker():
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    while True:
        phrase = speak_queue.get()
        if phrase is None:
            break
        print("[говорю]", phrase)
        speaker.Speak(phrase)
        speak_queue.task_done()

def speak(text):
    speak_queue.put(text)
