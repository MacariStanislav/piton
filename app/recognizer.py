import speech_recognition as sr
from app.voice import speak
from app.commands import CommandHandler
from config.allConfig import opts

_recognizer = None
_microphone = None
_handler = None

def initialize_handler():
    global _handler
    if _handler is None:
        _handler = CommandHandler(opts)

def handle_text_command(text: str):
    global _handler
    initialize_handler()

    voice = text.lower().strip()
    print('[обработка]', voice)

   
    if not _handler.active_listening and not _handler.is_activation_phrase(voice):
        print('[ассистент не активен]')
        return

    if not _handler.active_listening:
        _handler.activate_listening()

    _handler.handle_command(voice)

def _callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('[распознано]', voice)
        handle_text_command(voice)
    except sr.UnknownValueError:
        print('[голос не распознан]')
    except Exception as e:
        print('Ошибка в callback:', e)

def start_recognizer_background():
    global _recognizer, _microphone
    _recognizer = sr.Recognizer()
    _microphone = sr.Microphone()

    with _microphone as source:
        _recognizer.adjust_for_ambient_noise(source)

    stop = _recognizer.listen_in_background(_microphone, _callback)
    return stop

def start_console_worker():
    import threading
    def worker():
        while True:
            try:
                cmd = input(">>> ")
                handle_text_command(cmd)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print("Ошибка консольной команды:", e)
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t
