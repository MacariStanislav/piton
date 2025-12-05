import datetime
import os
import subprocess
from fuzzywuzzy import fuzz
from app.voice import speak
from app.browser import (
    open_url, play_music_track, open_instagram, 
    yt_playlist, play_current_video, open_youtube,
    open_google, search_google, search_youtube, 
    
)

class CommandHandler:
    def __init__(self, opts):
        self.opts = opts
        self.active_listening = False
        self.command_map = {
            "ctime": self.cmd_ctime,
            "music": self.cmd_music,
            "telegram_app": self.cmd_telegram_app,
            "instagram": self.cmd_instagram,
            "vscode": self.cmd_vscode,
            "next": self.cmd_next,
            "youtube": self.cmd_youtube,
            "google": self.cmd_google,
            "news": self.cmd_news,
            "activate": self.activate_listening,
            "deactivate": self.deactivate_listening,
            "calc": self.cmd_calc,
            "notepad": self.cmd_notepad,
            "explorer": self.cmd_explorer,
            "exit": self.cmd_exit,
           
           
        }

    def clean_text(self, text: str) -> str:
        for name in self.opts['name']:
            text = text.replace(name, '')
        for t in self.opts['tbr']:
            text = text.replace(t, '')
        return ' '.join(text.strip().split())

    def speak_and_log(self, text: str):
        print(f"[ответ]: {text}")
        speak(text)

    def recognize_cmd(self, cmd: str) -> str | None:
        cmd_clean = self.clean_text(cmd.lower())
        threshold = 80  
        best_match = {'cmd': None, 'percent': 0}

        for key, aliases in self.opts['cmds'].items():
            for alias in aliases:
                ratio = fuzz.ratio(cmd_clean, alias)  
                if ratio > best_match['percent']:
                    best_match['cmd'] = key
                    best_match['percent'] = ratio

        if best_match['percent'] >= threshold:
            return best_match['cmd']
        return None

    def is_activation_phrase(self, text: str) -> bool:
        return any(name in text for name in self.opts['name'])

    def handle_command(self, text: str):
        if not self.active_listening and not self.is_activation_phrase(text):
            print('[ассистент не активен]')
            return

        if not self.active_listening:
            self.activate_listening()

        cleaned = self.clean_text(text)
        cmd_key = self.recognize_cmd(cleaned)
        if cmd_key and cmd_key in self.command_map:
            self.command_map[cmd_key](original_text=text)
        else:
            self.speak_and_log("Команда не распознана.")

    def cmd_ctime(self, original_text=None, *_):
        now = datetime.datetime.now()
        self.speak_and_log(f"Сейчас {now.hour}:{now.minute:02d}, сэр.")

    def cmd_music(self, original_text=None, *_):
        from app.music import ask_for_music_track
        track_name = ask_for_music_track(console_mode=False)
        if track_name:
            play_music_track(track_name)

    def cmd_telegram_app(self, original_text=None, *_):
        self.speak_and_log("Открываю приложение Telegram Desktop.")
        try:
            telegram_path = r"C:\Users\stasm\AppData\Roaming\Telegram Desktop\Telegram"
            subprocess.Popen([telegram_path])
        except Exception as e:
            self.speak_and_log(f"Ошибка при открытии Telegram: {str(e)}")

    def cmd_instagram(self, original_text=None, *_):
        self.speak_and_log("Открываю Инстаграм.")
        open_instagram()

 

    def cmd_vscode(self, original_text=None, *_):
        self.speak_and_log("Открываю Visual Studio Code.")
        try:
            vscode_path = r"D:\Microsoft VS Code\Code"
            subprocess.Popen([vscode_path])
        except Exception as e:
            self.speak_and_log(f"Ошибка при открытии VS Code: {str(e)}")

    def cmd_next(self, original_text=None, *_):
        if yt_playlist['ids']:
            if yt_playlist['idx'] + 1 < len(yt_playlist['ids']):
                yt_playlist['idx'] += 1
                self.speak_and_log(f"Переключаю на следующий трек: номер {yt_playlist['idx'] + 1}.")
                play_current_video()
            else:
                self.speak_and_log("Это последний трек в плейлисте.")
        else:
            self.speak_and_log("Плейлист пуст, сначала включите музыку.")

    def cmd_youtube(self, original_text=None, *_):
        if original_text:
            cmd_words = self.opts['cmds'].get('youtube', [])
            query = original_text.lower()
            
            for keyword in cmd_words:
                query = query.replace(keyword, '')
            
            for name in self.opts['name']:
                query = query.replace(name.lower(), '')
            
            query = query.strip()
            
            if query:
                self.speak_and_log(f"Ищу на YouTube: {query}")
                search_youtube(query)
            else:
                self.speak_and_log("Открываю YouTube.")
                open_youtube()
        else:
            self.speak_and_log("Открываю YouTube.")
            open_youtube()

    def cmd_google(self, original_text=None, *_):
        if original_text:
           
            cmd_words = self.opts['cmds'].get('google', [])
            query = original_text.lower()
            
            
            for keyword in cmd_words:
                query = query.replace(keyword, '')
            
           
            for name in self.opts['name']:
                query = query.replace(name.lower(), '')
            
            query = query.strip()
            
            if query:
                self.speak_and_log(f"Ищу в Google: {query}")
                search_google(query)
            else:
                
                self.speak_and_log("Открываю Google.")
                open_google()
        else:
            self.speak_and_log("Открываю Google.")
            open_google()

    def cmd_news(self, original_text=None, *_):
        self.speak_and_log("Показываю последние новости.")
        open_url("https://news.google.com/")

    def cmd_calc(self, original_text=None, *_):
        self.speak_and_log("Открываю калькулятор.")
        os.system("calc")

    def cmd_notepad(self, original_text=None, *_):
        self.speak_and_log("Открываю блокнот.")
        os.system("notepad")

    def cmd_explorer(self, original_text=None, *_):
        self.speak_and_log("Открываю проводник.")
        os.system("explorer")

    def cmd_exit(self, original_text=None, *_):
        self.speak_and_log("Завершаю работу.")
        import sys
        sys.exit(0)

    def activate_listening(self, original_text=None, *_):
        self.active_listening = True

    def deactivate_listening(self, original_text=None, *_):
        self.active_listening = False
        self.speak_and_log("Режим прослушивания выключен.")

    def handle_text_command(self, text: str):
        if not self.active_listening and not self.is_activation_phrase(text):
            print("[ассистент не активен]")
            return

        if not self.active_listening:
            self.activate_listening()

        cleaned = self.clean_text(text)
        cmd_key = self.recognize_cmd(cleaned)

        if cmd_key and cmd_key in self.command_map:
            self.command_map[cmd_key](original_text=text)
        else:
            self.speak_and_log("Команда не распознана.")