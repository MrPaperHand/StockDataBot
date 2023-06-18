import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# Gets rid of annoying warnings
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options)

# Goes to this site
driver.get("https://www.nasdaq.com/market-activity/stocks/screener")

action = ActionChains(driver)

# Clicks accept for the cookies thing
ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)
element = WebDriverWait(driver, 2000, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
element.click()

# Clicks NYSE Checkbox
element = WebDriverWait(driver, 2000, ignored_exceptions=ignored_exceptions)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR,".nasdaq-screener__radio-box--exchange-item-NYSE .radioCircle")))
element.click()

# Scroll to Apply Button
driver.execute_script("window.scrollTo(0, 1000)") 

# Clicks Apply
element = WebDriverWait(driver, 2000, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".nasdaq-screener__form-button--apply")))
element.click()

spreadsheet = open("spreadsheet.txt",'w')

for t in range(1,3):
    for i in range(1,26):
        driver.fullscreen_window()
        # if i >= 9 scroll page down to lower half
        if i >= 9:
            driver.execute_script("window.scrollTo(0,1000)")

        element = WebDriverWait(driver,2000,ignored_exceptions=ignored_exceptions)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,(f'.nasdaq-screener__row:nth-child({i}) > .nasdaq-screener__cell--name > .firstCell'))))
        element.click()

        #element = WebDriverWait(driver,2000,ignored_exceptions=ignored_exceptions)\
        #            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,".symbol-page-header__name--symbol")))
        element = driver.find_element(By.CSS_SELECTOR,".symbol-page-header__name--symbol")

        text = element.text
        spreadsheet.write(text+"\n")

        driver.back()

        # Clicks NYSE Checkbox
        element = WebDriverWait(driver,2000,ignored_exceptions=ignored_exceptions)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,".nasdaq-screener__radio-box--exchange-item-NYSE .radioCircle")))
        element.click()

        # Scroll to Apply Button
        driver.execute_script("window.scrollTo(0, 1000)") 

        # Clicks Apply
        element = WebDriverWait(driver,2000,ignored_exceptions=ignored_exceptions)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,".nasdaq-screener__radio-box--exchange-item-NYSE .radioCircle")))
        element.click()

        #if i === 25 go to next page and set i to 0.
        if i == 25:
            driver.fullscreen_window()
            driver.execute_script("window.scrollTo(0, 1000)")
            
            element = WebDriverWait(driver,2000,ignored_exceptions=ignored_exceptions)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,(f'.nasdaq-screener__row:nth-child({i}) > .nasdaq-screener__cell--name > .firstCell'))))
            element.click()

            # Clicks NYSE Checkbox
            element = WebDriverWait(driver, 2000, ignored_exceptions=ignored_exceptions)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR,".nasdaq-screener__radio-box--exchange-item-NYSE .radioCircle")))
            element.click()

            # Scroll to Apply Button
            driver.execute_script("window.scrollTo(0, 1000)") 

            # Clicks Apply
            element = WebDriverWait(driver, 2000, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".nasdaq-screener__form-button--apply")))
            element.click()

            time.sleep(2)   

        
