import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

app = Flask(__name__)


def get_article_of_the_day():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Explicit Chrome binary path
    chrome_options.binary_location = os.path.join(
        os.getcwd(),
        "chrome/opt/google/chrome/chrome"
    )

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=chrome_options
    )

    try:
        driver.get("https://en.wikipedia.org/wiki/Main_Page")
        article_link = driver.find_element(By.CSS_SELECTOR, "#mp-tfa p b a")
        return {"title": article_link.text, "url": article_link.get_attribute("href")}
    finally:
        driver.quit()


@app.route("/")
def aotd():
    return jsonify(get_article_of_the_day())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)