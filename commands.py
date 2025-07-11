import datetime
from fuzzywuzzy import fuzz
from voice import speak
from browser import yt_playlist, play_current_video, open_url
from config.allConfig import opts

gpt_enabled = False

def clean_text(text):
    for name in opts["name"]:
        text = text.replace(name, "")
    for t in opts["tbr"]:
        text = text.replace(t, "")
    return ' '.join(text.strip().split())

def recognize_cmd(cmd):
    RC = {"cmd": "", "percent": 0}
    threshold = 55 
    for c, v in opts["cmds"].items():
        for x in v:
         
            ratios = [
                fuzz.ratio(cmd, x),
                fuzz.partial_ratio(cmd, x),
                fuzz.token_sort_ratio(cmd, x)
            ]
            max_ratio = max(ratios)
            if max_ratio > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = max_ratio
    return RC if RC["percent"] >= threshold else {"cmd": "", "percent": 0}

def execute_cmd(cmd, original_text=None):
    global gpt_enabled

    def speak_and_log(text):
        print(f"[ответ]: {text}")
        speak(text)

    if cmd == "ctime":
        now = datetime.datetime.now()
        speak_and_log(f"Сейчас {now.hour}:{now.minute:02d}, сэр.")
    
    elif cmd == "music":
        from recognizer import ask_for_music_track
        speak_and_log("Хорошо, скажите название трека.")
        ask_for_music_track()
    elif cmd == "telegram":
        from browser import open_telegram
        open_telegram()
    elif cmd == "instagram":
        from browser import open_instagram
        open_instagram()
    elif cmd == "next":
        if yt_playlist["ids"]:
            if yt_playlist["idx"] + 1 < len(yt_playlist["ids"]):
                yt_playlist["idx"] += 1
                speak_and_log(f"Переключаю на следующий трек: номер {yt_playlist['idx'] + 1}.")
                play_current_video()
            else:
                speak_and_log("Это последний трек в плейлисте.")
        else:
            speak_and_log("Плейлист пуст, сначала включите музыку.")
    
    elif cmd == "youtube":
        speak_and_log("Открываю YouTube для вас.")
        open_url("https://www.youtube.com/")
    
    elif cmd == "legend":
        speak_and_log("Вы легенда, сэр! Михаил — просто шутка.")
    
    elif cmd == "google":
        if original_text:
          
            query = original_text.lower()
          
            for keyword in opts["cmds"].get("google", []):
                query = query.replace(keyword, "")
            query = query.strip()
            if query:
                speak_and_log(f"Ищу в Google: {query}")
                open_url(f"https://www.google.com/search?q={query}")
            else:
                speak_and_log("Что именно искать в Google?")
        else:
            speak_and_log("Открываю главную страницу Google.")
            open_url("https://www.google.com")
    
    elif cmd == "news":
        speak_and_log("Показываю последние новости.")
        open_url("https://news.google.com/")
    
    elif cmd == "gpt_on":
        gpt_enabled = True
        speak_and_log("Режим GPT включён. Задавайте вопросы.")
    
    elif cmd == "gpt_off":
        gpt_enabled = False
        speak_and_log("Режим GPT отключён.")
    
    # else:
    #     if gpt_enabled and original_text:
    #         speak_and_log("Обрабатываю запрос через GPT...")
    #         # gpt_response = ask_gpt(original_text)
    #         # speak_and_log(gpt_response)
    #     else:
    #         speak_and_log("Команда не распознана, попробуйте еще раз.")
