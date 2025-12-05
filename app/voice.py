

import queue
import threading
import pythoncom
import win32com.client

_speak_queue = queue.Queue()
_speak_thread = None


def _speak_worker():
  
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    try:
        while True:
            phrase = _speak_queue.get()
            if phrase is None:
                break
            print('[говорю]', phrase)
            try:
                speaker.Speak(phrase)
            except Exception as e:
                print('Ошибка TTS:', e)
            _speak_queue.task_done()
    finally:
        pythoncom.CoUninitialize()


def start_speak_worker():
    global _speak_thread
    if _speak_thread and _speak_thread.is_alive():
        return
    _speak_thread = threading.Thread(target=_speak_worker, daemon=True)
    _speak_thread.start()


def stop_speak_worker():

    _speak_queue.put(None)
    if _speak_thread:
        _speak_thread.join(timeout=2)


def speak(text: str):
   
    if not isinstance(text, str):
        text = str(text)
    _speak_queue.put(text)


