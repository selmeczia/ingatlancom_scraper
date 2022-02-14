from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd


ad_data = pd.DataFrame()

ser = Service("C:\Program Files (x86)\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

url = "https://ingatlan.com/lista/elado+lakas+xiii-ker"
driver.get(url)

time.sleep(2)
boxes = driver.find_elements(By.CLASS_NAME, "listing__parameters")
i = 1
scroll = 0
for box in boxes:
    time.sleep(1)

    scroll = scroll + 150
    driver.execute_script(f"window.scrollTo(0, {scroll})")
    box.click()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    main_parameters = driver.find_element(By.CLASS_NAME, "parametersContainer").text.split("\n")
    detailed_par_names = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[1]/div[2]/div[1]/div[1]/div[1]/dl").find_elements(By.CLASS_NAME, "parameterName")
    detailed_par_values = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[1]/div[2]/div[1]/div[1]/div[1]/dl").find_elements(By.CLASS_NAME, "parameterValue")

    detailed_pars = dict(zip([element.text for element in detailed_par_names], [element.text for element in detailed_par_values]))


    parameter_dict = dict(zip(main_parameters[::2], main_parameters[1::2]))
    parameter_dict.update(detailed_pars)
    i += 1
    ad_data = ad_data.append(pd.DataFrame(parameter_dict, index=[i,]), ignore_index=True)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

ad_data