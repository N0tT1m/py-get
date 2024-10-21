import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# FlareSolverr configuration
FLARESOLVERR_URL = "http://localhost:8191/v1"


def solve_cloudflare(url, method="GET", data=None):
    payload = {
        "cmd": "request.{0}".format(method.lower()),
        "url": url,
        "maxTimeout": 60000
    }
    if data:
        payload["postData"] = json.dumps(data)

    response = requests.post(FLARESOLVERR_URL, json=payload)
    return response.json()

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_chrome_driver():
    options = Options()

    options = Options()
    options.add_argument("--verbose")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)

    options.add_argument(r"user-data-dir=C:\Users\Nathan\AppData\Local\Google\Chrome\User Data\Profile 1")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Path to ChromeDriver, not Chrome browser
    chromedriver_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update this path
    if not os.path.exists(chromedriver_path):
        logger.error(f"ChromeDriver not found at {chromedriver_path}")
        return None

    service = Service(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("Chrome driver initialized successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize Chrome driver: {e}")
        return None

def navigate_to_page(driver, url, timeout=10):
    if driver is None:
        logger.error("Driver is not initialized")
        return False

    try:
        logger.info(f"Attempting to navigate to {url}")
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logger.info(f"Successfully navigated to {url}")
        return True
    except TimeoutException:
        logger.error(f"Timed out while trying to load {url}")
        logger.debug(f"Current URL: {driver.current_url}")
        logger.debug(f"Page source: {driver.page_source[:500]}...")  # Log first 500 chars of page source
        return False
    except WebDriverException as e:
        logger.error(f"An error occurred while navigating to {url}: {e}")
        return False

def download_freeuse_mylf_file(name, url):
    time.sleep(30)

    output_file = f"/home/timmy/externalhd/teamskeet/freeuse-mylf/{name}.mp4"

    # Use FlareSolverr to bypass Cloudflare
    solved_response = solve_cloudflare(url)
    if solved_response["status"] == "ok":
        content = requests.get(url, headers=solved_response["solution"]["headers"]).content
        with open(output_file, 'wb') as file:
            file.write(content)
    else:
        print(f"Failed to bypass Cloudflare for {url}")


def get_freeuse_mylf_movies():
    driver = setup_chrome_driver()
    if driver:
        username = os.environ.get("TEAMSKEET_USERNAME", "")
        password = os.environ.get("TEAMSKEET_PASSWORD", "")

        url = "https://members.mylf.com/oauth/login"

        try:
            driver.get(url)
            time.sleep(5)  # Wait for 5 seconds
            print(f"Current URL: {driver.current_url}")

            username_elem = driver.find_element(By.NAME, "email")
            time.sleep(30)
            username_elem.send_keys(username)

            password_elem = driver.find_element(By.NAME, "password")
            time.sleep(30)
            password_elem.send_keys(password)

            input("Press Enter to continue...")

            time.sleep(10)

            site = "https://members.mylf.com/site/freeuse-milf"
            driver.get(site)

            links = driver.find_elements(By.XPATH, "//a[contains(@class, 'card--movie__thumnbail-wrapper')]")
            for link in links:
                href = link.get_attribute("href")
                print(href)

                if "https://members.mylf.com/m/" in href:
                    print(link)
                    add_shoplyfter_mylf_movie(href)  # This function needs to be implemented
            else:
                print("Failed to bypass Cloudflare")

        finally:
            driver.quit()


def download_freeuse_mylf_movies():
    movies = get_freeuse_mylf_movies()  # This function needs to be implemented

    username = os.environ.get("TEAMSKEET_USERNAME", "")
    password = os.environ.get("TEAMSKEET_PASSWORD", "")

    url = "https://members.mylf.com/oauth/login"

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(r"user-data-dir=C:\Users\Nathan\AppData\Local\Google\Chrome\User Data\Profile 1")

    driver = webdriver.Chrome(options=options)

    try:
        # Use FlareSolverr to bypass Cloudflare
        solved_response = solve_cloudflare(url)
        if solved_response["status"] == "ok":
            driver.get(url)
            for cookie in solved_response["solution"]["cookies"]:
                driver.add_cookie(cookie)

            username_elem = driver.find_element(By.NAME, "email")
            username_elem.send_keys(username)

            password_elem = driver.find_element(By.NAME, "password")
            password_elem.send_keys(password)

            input("Press Enter to continue...")

            time.sleep(10)

            for movie in movies:
                time.sleep(10)
                driver.get(movie)
                time.sleep(10)

                movie_title_element = driver.find_element(By.XPATH, "//h1[contains(@class, 'movie-details__h1')]")
                movie_title = movie_title_element.text

                output_file = f"/home/timmy/externalhd/teamskeet/freeuse-mylf/{movie_title}.mp4"

                if not os.path.exists(output_file):
                    movie_id = movie.replace("https://members.mylf.com/m/", "")
                    url = f"https://members.teamskeet.com/movie/download/video?id={movie_id}&resolution=2160"

                    # Use FlareSolverr for the download URL
                    solved_download = solve_cloudflare(url)
                    if solved_download["status"] == "ok":
                        driver.get(url)
                        time.sleep(30)

                        download = driver.find_element(By.XPATH, "//a[contains(@class, 'url')]")
                        download_url = download.get_attribute("href")

                        download_freeuse_mylf_file(movie_title, download_url)
                    else:
                        print(f"Failed to bypass Cloudflare for {url}")

                time.sleep(10)
        else:
            print("Failed to bypass Cloudflare")

    finally:
        driver.quit()



if __name__ == "__main__":
    get_freeuse_mylf_movies()
    # download_freeuse_mylf_movies()