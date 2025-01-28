from flask import Flask, jsonify


import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)


def get_article_of_the_day():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if "RENDER" in os.environ:
        # Running on Render -> We installed chromium-chromedriver via apt-get
        service = Service("/usr/bin/chromedriver")
    else:
        # Running locally -> use webdriver_manager or your local hardcoded path
        # service = Service(r"C:\Users\PC\.wdm\drivers\chromedriver\win64\130...\chromedriver.exe")
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    aotd = driver.find_element("id", "mp-tfa").text
    driver.quit()
    return aotd

@app.route("/")
def aotd():
    return jsonify(get_article_of_the_day())

if __name__ == "__main__":
    app.run()