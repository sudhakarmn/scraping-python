from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_savaari():
    # Set up Chrome options for headless browsing (no GUI)
    options = Options()
    #options.add_argument("--headeless") # run browser in backgroup
    options.add_argument("-disable-gpu") # Disbale GPU acceleration
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("window-size=1920.1080") # Set broswer window size
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)") # Spoof user-agent to mimic real browser
    driver = webdriver.Chrome(options=options)

    url = "https://www.savaari.com/"
    driver.get(url)
    time.sleep(3)

    try:
        pickup_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID,"pickupInput"))
        )
        pickup_dropdown.click()
        time.sleep(1)

        pickup_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,"//span[contains(text(), 'Bangalore, Karnataka')]"))
        )
        pickup_option.click()
        time.sleep(1)

        
    # Click on the drop city dropdown
        drop_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropInput"))
        )
        drop_dropdown.click()
        time.sleep(1)

        # Select Chennai from the dropdown
        drop_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Chennai, Tamil Nadu')]"))
        )
        drop_option.click()
        time.sleep(1)

        search_button = driver.find_element(By.XPATH, '//button[@class="book-button btn"]')
        search_button.click()
        time.sleep(5) 
        #find the car list container
        car_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='col-12 col carListHolder']"))
        )

        cars = car_list.find_elements(By.CLASS_NAME,"ng-star-inserted")
        data = []

        for car in cars:
            #print(car.get_attribute("outerHTML"))
            try:
                car_name_ele = car.find_element(By.XPATH,".//div[@class='car-name d-flex align-items-center']/span")

                print(car_name_ele.text)
                
                car_name = car_name_ele.text.strip()

                car_price_ele = car.find_element(By.CLASS_NAME,"price-current")
                car_price = car_price_ele.text.strip()

                data.append({"Car": car_name,"Price": car_price})
            except Exception as e:
                continue
        print(data)
        df = pd.DataFrame(data)
        df.to_csv("data/savaari_car_prices.csv", index=False)
    except Exception as e:
        print(f"Error during Scraping {e}\n")
    
    finally:
        driver.quit()
