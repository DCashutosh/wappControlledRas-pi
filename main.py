from wapp_init import Wapp_init
from wapp_apps import Wapp_apps
from cameraController import CameraController
from servoController import ServoController
from osController import OsController

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import config as Config
import time as time
import re

#user-setup
user = input("Please provide the user(Contact) : ")

if(user.startswith("+1")):
    formatted_user = f"{user[:2]}({user[2:5]}){user[5:8]}-{user[8:]}"
elif(user.startswith("+91")):
    formatted_user = f"{user[:3]} {user[3:8]} {user[8:]}"

# print(formatted_user)
cameraControl = CameraController()
servoControl = ServoController()
osControl = OsController()


def processRequest(cmd, img_counter, vdo_counter):
    Wapp_apps.send_msg("Processing Request !!!")
    if(cmd == "instashot"):

        file_name = Config.image_folder+f'image_{img_counter}'
        cameraControl.capture_image(file_name)
        Wapp_apps.send_file(file_name)
        img_counter = img_counter+1

    elif(re.search("video",cmd)):

        file_name = Config.video_folder+f'video_{vdo_counter}'
        match = re.search(r'\d+', cmd)
        duration = int(match.group())

        if(duration <= 60):
            cameraControl.record_video(file_name)
            Wapp_apps.send_file(file_name)
            vdo_counter = vdo_counter+1
        else:
            print(f'Vidoe duration not valid : {duration}')
            Wapp_apps.send_msg("Does not support video recording over 60 seconds")

    elif(re.search("image_angle",cmd)):

        file_name = Config.image_folder+f'image_{img_counter}'
        match = re.search(r'[+-]?\d+', cmd)
        angle = int(match.group())

        if(180 >= angle >= -180):
            servoControl.rotate_servo_angle(angle)
            cameraControl.capture_image(file_name)
            Wapp_apps.send_file(file_name)
            img_counter = img_counter+1
        else:
            print(f'Angle value not recognizable : {angle}')
            Wapp_apps("Invalid Angle Value.")
    
    elif(cmd == "video 180 degree"):

        file_name = Config.video_folder+f'video_{vdo_counter}'
        cameraControl.record_180video(file_name)
        Wapp_apps.send_file(file_name)
        vdo_counter = vdo_counter+1
    
    elif(re.search("End session",cmd)):
        Wapp_apps.send_msg("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
        time.sleep(5)
        osControl.clear_folder(Config.image_folder)
        time.sleep(5)
        osControl.clear_folder(Config.video_folder)
        driver.quit()
    
    else:
        Wapp_apps.send_msg("Invalid Command")

def check_continue(cmd):
    if(re.search("continue",cmd)):
        Wapp_apps.send_msg("Please provide the next command")
        time.sleep(20)
    else:
        Wapp_apps.send_msg("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
        time.sleep(5)
        osControl.clear_folder(Config.image_folder)
        time.sleep(5)
        osControl.clear_folder(Config.video_folder)
        driver.quit()
            



#chrome-driver-setup
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={Config.profile_path}")
options.add_argument(f"profile-directory={Config.profile}")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

service = Service(executable_path=Config.exec_path)
driver = webdriver.Chrome(service=service, options=options)

#Can also set this so it will also take the sender dynamically
setup = Wapp_init(Config.def_sender,driver)
apps = Wapp_apps(formatted_user,driver)
img_cnt = 0
vdo_cnt = 0

setup.open_whatsapp()
time.sleep(5)

if(setup.is_element_present(Config.link_mobile)):
    setup.setup_sender(Config.def_sender)

apps.search_contact()
time.sleep(5)
apps.send_msg(Config.def_msg)
time.sleep(2)
apps.send_msg(Config.instruction)
time.sleep(60)


while True:
    cmd = apps.read_msg().pop()
    processRequest(cmd,img_cnt,vdo_cnt)
    time.sleep(5)
    Wapp_apps.send_msg("Please type (continue) to continue the session")
    time.sleep(15)
    nxt_cmd = apps.read_msg().pop()
    check_continue(nxt_cmd)


# text = apps.read_msg()
# print(text.pop())
# apps.send_file("E:/flipped_image_1x.jpg")
# time.sleep(10)
# driver.quit()





