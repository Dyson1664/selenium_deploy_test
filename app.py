from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)


def get_article_of_the_day():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get("https://en.wikipedia.org/wiki/Main_Page")

        # Wait for the main container and get first article link
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mp-tfa"))
        )

        article_link = driver.find_element(
            By.XPATH, "//div[@id='mp-tfa']//p//a[1]"
        )

        return {
            "title": article_link.text,
            "url": article_link.get_attribute("href")
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return {"error": "Failed to fetch article"}
    finally:
        driver.quit()


@app.route("/")
def aotd():
    return jsonify(get_article_of_the_day())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)