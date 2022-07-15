from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(8)
wait = WebDriverWait(driver, 10)


def get_info():
    # Get the region
    region_list = []

    regions = driver.find_elements(
        By.XPATH, "/html/body/div[1]/div[4]/div[1]/table/tbody/tr/td[2]/h3")
    for region in regions:
        region_list.append(region.text)

    # Get the price per sqm
    price_list = []

    prices = driver.find_elements(
        By.XPATH, "/html/body/div[1]/div[4]/div[1]/table/tbody/tr/td[2]/div/span[2]")
    for price in prices:
        price_list.append(price.text)

    ares_list = []

    ares = driver.find_elements(
        By.XPATH, "/html/body/div[1]/div[4]/div[1]/table/tbody/tr/td[4]")
    for are in ares:
        ares_list.append(are.text)

    df = pd.DataFrame(list(zip(region_list, price_list, ares_list)),
                      columns=['Region', 'Price', 'Ares'])
    return df


df = pd.DataFrame()

i = 1
while i in range(61):
    website = "https://en.aruodas.lt/butai/vilniuje/puslapis/" + \
        str(i)+"/?FHouseState=full"
    driver.get(website)
    element = wait.until(EC.element_to_be_clickable((
        By.XPATH, '/ html/body/div[1]/div[4]/div[1]/table/tbody/tr/td[2]/h3')))
    df = pd.concat([df, get_info()], ignore_index=True)
    i += 1
print(df)

df.to_csv('file.csv', encoding='utf-8')
