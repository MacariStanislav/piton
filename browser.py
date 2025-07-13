import time
import re
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from voice import speak
import subprocess
driver = None
yt_playlist = {"ids": [], "idx": -1}


def init_browser():
    global driver


    if driver:
        try:
      
            driver.current_url
            return
        except WebDriverException:
            try:
                driver.quit()
            except Exception:
                pass
            driver = None  

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.maximize_window()

def open_url(url):
    global driver  
    init_browser()
    try:
        driver.get(url)
    except Exception:
        speak("Ошибка при открытии страницы. Перезапускаю браузер.")
        try:
            driver.quit()
        except:
            pass
        driver = None
        init_browser()
        driver.get(url)



def get_youtube_ids(query, limit=5):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    resp = requests.get(search_url)
    if resp.status_code == 200:
        ids = re.findall(r"watch\?v=(\S{11})", resp.text)
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
    idx = yt_playlist["idx"]
    ids = yt_playlist["ids"]
    if 0 <= idx < len(ids):
        url = f"https://www.youtube.com/watch?v={ids[idx]}"
        driver.get(url)
        time.sleep(4)
        driver.execute_script("""
            var video = document.querySelector('video');
            if (video) {
                video.play();
            }
        """)
        speak(f"Воспроизводится трек номер {idx + 1}")
    else:
        speak("Нет доступных треков.")




def open_telegram():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_path = r"C:\Users\stasm\AppData\Local\Google\Chrome\User Data\Default"  
    profile_dir = "Default" 
    url = "https://web.telegram.org/"

    subprocess.Popen([
        chrome_path,
        f'--profile-directory={profile_dir}',
        f'--user-data-dir={profile_path}',
        url
    ])

def open_instagram():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_path = r"C:\Users\stasm\AppData\Local\Google\Chrome\User Data\Default"  
    profile_dir = "Default"  
    url = "https://www.instagram.com/"

    subprocess.Popen([
        chrome_path,
        f'--profile-directory={profile_dir}',
        f'--user-data-dir={profile_path}',
        url
    ])
