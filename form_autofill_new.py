import threading
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login():
    username = "abc@gmail.com"
    password = "asdf"
    
    #HTML XPath 
    username_input = '//*[@id="wrap-login"]/form/div[1]/input'
    password_input = '//*[@id="wrap-login"]/form/div[2]/input'
    login_submit = '//*[@id="register"]'

    driver.find_element_by_xpath(username_input).click()
    driver.find_element_by_xpath(username_input).send_keys(username)

    driver.find_element_by_xpath(password_input).click()
    driver.find_element_by_xpath(password_input).send_keys(password)

    driver.find_element_by_xpath(login_submit).click()
    time.sleep(2)


def dashboard():
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
    test_button = '/html/body/div[2]/div/div/div[6]/div/a/button'
    driver.find_element_by_xpath(test_button).click()
    time.sleep(1)

#test(section number, number of questions)
def test(i, n):
    for x in range(1, n):
        rand = random.choice(['2', '3', '4', '5', '6'])
        #rand = random.randrange(2,7)
        choice_input = '/html/body/div[2]/div/form/div[' +str(i)+']/div['+str(x)+']/div['+rand+']/div/input'
        # print(rand)
        driver.find_element_by_xpath(choice_input).click()

    if(i != 10):
        driver.find_element_by_xpath(next_button).click()
        driver.find_element_by_tag_name(
            'body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(2)


if __name__ == '__main__':

    # connection
    # download chromedriver https://chromedriver.chromium.org/downloads and install
    chromedriver_location = "C:/Users/hp/Downloads/chromedriver"
    driver = webdriver.Chrome(chromedriver_location)
    #url of the website(flask run)
    driver.get('http://127.0.0.1:5000/')

    # login
    thread = threading.Thread(target=login())
    thread.start()
    thread.join()

    for z in range(0, 2):
        # dashboard
        thread = threading.Thread(target=dashboard())
        thread.start()
        thread.join()

        next_button = '/html/body/div[2]/div/form/div[11]/div/button[2]'

        thread = threading.Thread(target=test(1, 6))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(2, 8))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(3, 6))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(4, 9))
        thread.start()
        thread.join()
        
        thread = threading.Thread(target=test(5, 6))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(6, 8))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(7, 8))
        thread.start()
        thread.join()
    
        thread = threading.Thread(target=test(8, 6))
        thread.start()
        thread.join()

        thread = threading.Thread(target=test(9, 6))
        thread.start()
        thread.join() 
        
        thread = threading.Thread(target=test(10, 6))
        thread.start()
        thread.join()
        
        submit_button = '//*[@id="submit"]'
        driver.find_element_by_xpath(submit_button).click()

        time.sleep(1)
