import speech_recognition as sr
from voice import speak
from commands import clean_text, recognize_cmd, execute_cmd, recognize_hello, execute_hello
from browser import yt_playlist, play_current_video
from config.allConfig import opts
from browser import get_youtube_ids
def ask_for_music_track():
    yt_playlist["ids"], yt_playlist["idx"] = [], -1
    speak("Какой трек хотите?")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  
        print("Слушаю название трека...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5) 


    try:
        track_name = r.recognize_google(audio, language="ru-RU").lower()
        print(f"Распознано название трека: {track_name}")
        speak(f"Ищу трек {track_name} на YouTube.")

        ids = get_youtube_ids(track_name)
        if not ids:
            speak("Ничего не нашёл.")
            return
        yt_playlist["ids"] = ids
        yt_playlist["idx"] = 0
        play_current_video()
    except sr.UnknownValueError:
        speak("Не расслышал название трека, попробуйте ещё раз.")
    except Exception as e:
        speak(f"Ошибка при распознавании: {str(e)}")

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[распознано]", voice)

   
        if any(hello_phrase in voice for hello_phrase in opts["hello"]):
            cleaned = clean_text(voice)
            hello_data = recognize_hello(cleaned)
            execute_hello(hello_data["hell"], original_text=cleaned)
            
        elif any(name in voice for name in opts["name"]):
            cleaned = clean_text(voice)
            cmd_data = recognize_cmd(cleaned)
            execute_cmd(cmd_data["cmd"], original_text=cleaned)
        else:
            print("[Команда не для меня]")
    except sr.UnknownValueError:
        print("[голос не распознан]")
       
