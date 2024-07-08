from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config as Config

class Wapp_init:

    #whatsapp-sender-user(controller)
    sender = Config.def_sender
    driver = None

    def __init__(self,sender,driver):
        self.sender = sender
        self.driver = driver
    
    def open_whatsapp(self):

        # Open WhatsApp Web in a new tab
        print("opening whatsapp web")
        self.driver.execute_script("window.open('https://web.whatsapp.com', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(5)
    
    #pulling-verification-code to setup whatsapp sender
    def generateCode(self):
        code = ""
        for i in range(1,9):
            xpath = f'//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div/div/div[{i}]/span'
            element = self.driver.find_element(By.XPATH,xpath)
            code = code+element.text
        
        print("The final code is : "+code)

    #setting-up new whatsapp sender
    def setup_sender(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, Config.link_mobile))
        )

        link = self.driver.find_element(By.XPATH, Config.link_mobile)
        link.click()

        WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.XPATH, Config.sender_box))
        )

        input_number = self.driver.find_element(By.XPATH, Config.sender_box)
        input_number.send_keys(Config.def_sender + Keys.ENTER)

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, Config.code_box))
        )

        self.generateCode()
