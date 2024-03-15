import time
import redis
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():

    driver = webdriver.Chrome(
        service=ChromeService(
            ChromeDriverManager().install()
        )
    )
    driver.get("https://www.idealista.pt/")
    driver.quit()
    return f'Hello World! I have been seen X times.\n'
