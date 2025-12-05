import os
import time
import re
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.voice import speak
from pathlib import Path

driver = None
yt_playlist = {'ids': [], 'idx': -1}

def get_default_chrome_profile_path():
    username = os.getlogin()
    
    possible_paths = [
        Path(f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data'),
        Path(f'C:\\Пользователи\\{username}\\AppData\\Local\\Google\\Chrome\\User Data'),
        Path(f'C:\\Documents and Settings\\{username}\\Local Settings\\Application Data\\Google\\Chrome\\User Data'),
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"Найден профиль Chrome: {path}")
            return str(path)
    
    default_path = Path(f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data')
    print(f"Используется путь по умолчанию: {default_path}")
    return str(default_path)

def get_domain_name(url: str) -> str:
    """Получает красивое имя домена из URL"""
    try:
        if "//" in url:
            domain = url.split("//")[1].split("/")[0]
        else:
            domain = url.split("/")[0]
        
        domain = domain.replace("www.", "")
        
        domain_mapping = {
            "youtube.com": "Ютуб",
            "youtu.be": "Ютуб",
            "instagram.com": "Инстаграм",
            "telegram.org": "Телеграм",
            "web.telegram.org": "Телеграм",
            "google.com": "Гугл",
            "mail.google.com": "Гугл почта",
            "gmail.com": "Гугл почта",
            "facebook.com": "Фейсбук",
            "twitter.com": "Твиттер",
            "x.com": "Твиттер",
            "vk.com": "Вконтакте",
            "whatsapp.com": "Ватсап",
            "web.whatsapp.com": "Ватсап",
            "github.com": "Гитхаб",
            "linkedin.com": "ЛинкедИн",
            "reddit.com": "Реддит",
            "tiktok.com": "ТикТок",
            "discord.com": "Дискорд",
            "twitch.tv": "Твич",
            "netflix.com": "Нетфликс",
            "spotify.com": "Спотифай",
            "amazon.com": "Амазон",
            "ebay.com": "Ибэй",
            "aliexpress.com": "Алиэкспресс",
        }
        
        if domain in domain_mapping:
            return domain_mapping[domain]
        
        parts = domain.split(".")
        if len(parts) >= 2:
            return parts[0].capitalize()
        
        return domain
    except:
        return "сайт"

def is_chrome_running():
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], 
                              capture_output=True, text=True, shell=True)
        return "chrome.exe" in result.stdout
    except:
        return False

def open_url_in_existing_chrome(url: str):
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    
    if not os.path.exists(chrome_path):
        alt_paths = [
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                chrome_path = alt_path
                break
        else:
            speak("Не удалось найти Google Chrome на компьютере")
            return False
    
    try:
        cmd = [chrome_path, url]
        subprocess.Popen(cmd, shell=True)
        site_name = get_domain_name(url)
        speak(f'Открываю {site_name} в новой вкладке')
        return True
    except Exception as e:
        print(f"Ошибка при открытии вкладки в Chrome: {e}")
        return False

def open_browser_with_profile(url: str, profile_name: str = 'Default'):
   
    if is_chrome_running():
        if open_url_in_existing_chrome(url):
            return
    
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    
    if not os.path.exists(chrome_path):
        alt_paths = [
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                chrome_path = alt_path
                break
        else:
            speak("Не удалось найти Google Chrome на компьютере")
            return
    

    user_data_dir = get_default_chrome_profile_path()
    
 
    cmd = [
        chrome_path,
        f'--user-data-dir={user_data_dir}',
        f'--profile-directory={profile_name}',
        '--new-window',
        url
    ]
    
    try:
        print(f"Запуск Chrome: {' '.join(cmd)}")
        subprocess.Popen(cmd)
        site_name = get_domain_name(url)
        speak(f'Открываю {site_name} в новом окне')
    except Exception as e:
        print(f"Ошибка при запуске Chrome: {e}")
        speak("Не удалось открыть браузер")

def init_browser():
    global driver
    try:
        if driver:
            driver.current_url
            return
    except Exception:
        driver = None

    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
  
    chrome_options.add_argument(f'--user-data-dir={get_default_chrome_profile_path()}')
    chrome_options.add_argument('--profile-directory=Default')
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.maximize_window()
    except Exception as e:
        driver = None
        print(f"Ошибка запуска браузера: {e}")
        speak("Не удалось запустить браузер")

def open_url(url: str):

    if is_chrome_running():
        if open_url_in_existing_chrome(url):
            return
    
   
    init_browser()
    if driver is None:
        speak("Браузер не инициализирован")
        return
    try:
        driver.get(url)
    except Exception:
        speak('Ошибка при открытии страницы. Перезапускаю браузер.')
        try:
            driver.quit()
        except Exception:
            pass
        driver = None
        init_browser()
        if driver:
            driver.get(url)

def get_youtube_ids(query: str, limit: int = 5):
    search_url = f'https://www.youtube.com/results?search_query={query}'
    resp = requests.get(search_url)
    if resp.status_code == 200:
        ids = re.findall(r'watch\?v=(\S{11})', resp.text)
        unique = []
        for vid in ids:
            if vid not in unique:
                unique.append(vid)
            if len(unique) >= limit:
                break
        return unique
    return []

def play_current_video():
    init_browser()
    if driver is None:
        speak("Браузер не инициализирован")
        return
    idx = yt_playlist['idx']
    ids = yt_playlist['ids']
    if 0 <= idx < len(ids):
        url = f'https://www.youtube.com/watch?v={ids[idx]}'
        driver.get(url)
        time.sleep(4)
        driver.execute_script("""
            var video = document.querySelector('video');
            if (video) { video.play(); }
        """)
        speak(f'Воспроизводится трек номер {idx + 1}')
    else:
        speak('Нет доступных треков.')

def play_music_track(track_name: str):
    speak(f'Ищу трек "{track_name}" на YouTube...')
    video_ids = get_youtube_ids(track_name, limit=5)
    if not video_ids:
        speak("Не удалось найти трек на YouTube.")
        return
    yt_playlist['ids'] = video_ids
    yt_playlist['idx'] = 0
    speak(f'Найдено {len(video_ids)} треков. Воспроизвожу первый.')
    
    # Открываем YouTube в новой вкладке
    url = f'https://www.youtube.com/watch?v={video_ids[0]}'
    open_browser_with_profile(url, 'Default')


def open_instagram():
    open_browser_with_profile('https://www.instagram.com/', 'Default')

def open_youtube():
    open_browser_with_profile('https://www.youtube.com/', 'Default')

def open_google():
    open_browser_with_profile('https://www.google.com/', 'Default')

def search_google(query: str):
    search_url = f'https://www.google.com/search?q={query}'
    open_browser_with_profile(search_url, 'Default')

def search_youtube(query: str):
    search_url = f'https://www.youtube.com/results?search_query={query}'
    open_browser_with_profile(search_url, 'Default')
