from flask import Flask
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.worldometers.info")
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#c1"))
    )

app = Flask(__name__)
CORS(app)

KEY_LIST = ['current_world_population','births_this_year','births_today', 'deaths_this_year', 'deaths_tody', 'people_who_died_of_hunger_today', 'suicides_this_year']

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/all')
def all():
    # print(element)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    cgroup = soup.select(".counter-group")
    for counter in cgroup:
        c_head = counter.select_one("div.counter-heading")
        c_item = c_head.select_one("span.counter-item")
        if c_item:
            c_num = c_head.select("span.counter-number > span.rts-counter")
            num_list = [s.text for s in c_num]
            num=int(''.join(num_list).replace(',', ''))
            name = c_item.text.replace(' ', '_').lower()
            results[name] = num
            # print(name, num)

    return results


if __name__ == '__main__':
    app.run()