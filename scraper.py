import csv
import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_random_user_agent():
    try:
        with open('useragents.txt', newline='', encoding='utf-8') as txtfile:
            reader = csv.DictReader(txtfile, delimiter=';')
            return random.choice([row['useragent'] for row in reader])
    except FileNotFoundError:
        return None

def scrape_directory(url, output_file='company_names.txt', chrome_binary_path=None):
    options = webdriver.ChromeOptions()
    
    if chrome_binary_path:
        options.binary_location = chrome_binary_path

    user_agent = get_random_user_agent()
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)

        element_to_click = driver.find_element(By.CSS_SELECTOR, '#content > div > div:nth-child(3) > div > div.not-sidebar.stack > nav > a:nth-child(2)')
        element_to_click.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-item-ab')))

        updated_html = driver.page_source
        soup = BeautifulSoup(updated_html, 'html.parser')

        company_elements = soup.find_all(class_='result-item-ab exws2cl0 css-z34rva e1ri33r70')
        company_names = [element.text.strip() for element in company_elements]

        for name in company_names:
            print(name)

        with open(output_file, 'a', encoding='utf-8') as txt_file:
            for name in company_names:
                txt_file.write(name + '\n')

        print(f"Extraction successful. Data written to {output_file}")

    except Exception as e:
        print(f"Extraction failed: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    TARGET_URL = 'https://www.bbb.org/search?find_country=USA&find_entity=10049-000&find_id=1705_4600-1300&find_latlng=39.274642%2C-76.642327&find_loc=Baltimore%2C%20MD&find_text=Electrician&find_type=Category&page=1&sort=Relevance'
    CHROME_BIN = 'test_chrome\\chrome-win64\\chrome.exe'
    
    scrape_directory(TARGET_URL, chrome_binary_path=CHROME_BIN)