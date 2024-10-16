import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

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
    username = os.environ.get("TEAMSKEET_USERNAME", "")
    password = os.environ.get("TEAMSKEET_PASSWORD", "")

    url = "https://members.mylf.com/oauth/login"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Use FlareSolverr to bypass Cloudflare
        solved_response = solve_cloudflare(url)
        if solved_response["status"] == "ok":
            driver.get(url)
            for cookie in solved_response["solution"]["cookies"]:
                driver.add_cookie(cookie)

            username_elem = driver.find_element(By.NAME, "username")
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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Use FlareSolverr to bypass Cloudflare
        solved_response = solve_cloudflare(url)
        if solved_response["status"] == "ok":
            driver.get(url)
            for cookie in solved_response["solution"]["cookies"]:
                driver.add_cookie(cookie)

            username_elem = driver.find_element(By.NAME, "username")
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


def add_shoplyfter_mylf_movie(href):
    # This function needs to be implemented based on your specific requirements
    pass


if __name__ == "__main__":
    download_freeuse_mylf_movies()