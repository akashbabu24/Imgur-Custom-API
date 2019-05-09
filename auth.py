#!/usr/bin/env python3

'''
	Here's how you go about authenticating yourself! The important thing to
	note here is that this script will be used in the other examples so
	set up a test user with API credentials and set them up in auth.ini.
'''

from imgurpython import ImgurClient
from helpers import get_input, get_config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display

def authenticate():
	# Get client ID and secret from auth.ini
    config = get_config()
    config.read('auth.ini')

	#credentials from auth.ini file
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    img_username = config.get('credentials', 'imgur_username')
    img_password = config.get('credentials', 'imgur_password')

    client = ImgurClient(client_id, client_secret)

	# Authorization URL
    authorization_url = client.get_auth_url('pin')

	#selenium automation of logon to imgur and retrieval of PIN
	#options = Options()
        #options.headless = True
        #driver = webdriver.Firefox(options=options)
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.PhantomJS()
    driver.get(authorization_url)
    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.clear()
    username.send_keys(img_username)
    password.send_keys(img_password)
    driver.find_element_by_name("allow").click()
    timeout = 5
    try:
    	element_present = EC.presence_of_element_located((By.ID, 'pin'))
	WebDriverWait(driver,timeout).until(element_present)
	pin_element = driver.find_element_by_id('pin')
	pin_num = pin_element.get_attribute("value")
    except TimeoutException:
	print("Timeout exception")
	driver.close()

	#Retrive access and refresh tokens
    credentials = client.authorize(pin_num, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

	#return client that was authorized
    return client

# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
	authenticate()
