import speech_recognition as sr
from app.voice import speak

def ask_for_music_track(console_mode=False):
  
    if console_mode:
       
        track_name = input("Введите название трека: ").strip()
        if track_name:
            print(f"Трек введен: {track_name}")
            return track_name
        else:
            speak("Вы не ввели название трека.")
            return None

   
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        speak("Скажите название трека")
        print("Скажите название трека:")
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Время ожидания голоса истекло.")
            print("Время ожидания голоса истекло.")
            return None

    try:
        track = r.recognize_google(audio, language='ru-RU')
        print(f"Трек распознан: {track}")
        return track
    except sr.UnknownValueError:
        speak("Не удалось распознать трек")
        print("Не удалось распознать трек.")
        return None
    except Exception as e:
        speak("Ошибка распознавания трека")
        print("Ошибка распознавания:", e)
        return None
