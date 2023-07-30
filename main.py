import math
from selenium import webdriver
# element click intercept exception is raised when the element is not clickable
from selenium.common import ElementClickInterceptedException
# service is used to hide the logs
from selenium.webdriver.chrome.service import Service
# by is used to find the elements
from selenium.webdriver.common.by import By
import time as t
import os
from dotenv import load_dotenv

load_dotenv()

# setting the options for the webdriver to make it headless
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

similar_account = "https://www.instagram.com/yarnspirations/"
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


class Instafollower:
    def __init__(self):
        # service is used to hide the logs in the console window when the bot is running
        self.service = Service(executable_path="chromedriver.exe", log_path="NUL")
        # driver is used to run the bot in the background without opening the browser window and it is also used to
        # run the bot in the browser window by removing the options parameter in the webdriver function
        self.driver = webdriver.Chrome(options=options, service=self.service)
        # implicit wait is used to wait for the page to load before the bot starts running
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        # follows_count is used to count the number of follows the bot has done in the console window
        self.follows_count = 0

    def login(self):
        self.driver.get("https://www.instagram.com/")
        t.sleep(2)
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys(INSTAGRAM_USERNAME)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(INSTAGRAM_PASSWORD)
        login_button = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        login_button.click()
        t.sleep(5)

    # not_now function is used to click the not now button when the save login info and turn on notifications pop up
    def not_now(self):
        not_now_button = self.driver.find_element(By.XPATH,
                                                  '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div['
                                                  '2]/section/main/div/div/div/div/div')
        not_now_button.click()
        t.sleep(3)

        not_now_button_2 = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div['
                                                              '2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
        not_now_button_2.click()
        t.sleep(3)

    # find_followers function is used to find the followers of the similar account and click the followers button
    def find_followers(self):
        self.driver.get(similar_account)
        followers_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div['
                                                              '1]/div[1]/div[2]/div['
                                                              '2]/section/main/div/header/section/ul/li[2]/a')
        followers_button.click()
        t.sleep(5)

    def follow(self):
        # follower_count is used to get the number of followers of the similar account...replace is used to remove
        # the comma in the number of followers and convert it to an integer value and scroll_number is used to scroll
        # the window to the bottom of the page
        follower_count = int(
            self.driver.find_elements(By.CLASS_NAME, '_ac2a')[1].get_attribute('title').replace(',', ''))
        # math.ceil is used to round up the number of followers to the nearest integer value
        scroll_number = math.ceil(follower_count / 12) - 1
        scroll_window = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div['
                                                 '2]/div/div/div/div/div[2]/div/div/div[2]')
        # for loop is used to scroll the window to the bottom of the page and click the follow button for each follower
        for _ in range(scroll_number):
            # -12 is used to remove the last 12 followers from the list because they are not clickable
            follows_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div.x1dm5mii div._aacl')[-12:]
            # for loop is used to click the follow button for each follower and increment the follows_count by 1
            for follow in follows_buttons:
                try:
                    follow.click()
                # except is used to handle the ElementClickInterceptedException caused by the followers who are
                # not clickable
                except ElementClickInterceptedException:
                    self.driver.find_element(By.CLASS_NAME, '_a9_1').click()
                    pass
                # else is used to increment the follows_count by 1 if the follow button is clicked successfully
                else:
                    self.follows_count += 1
                # finally is used to wait for 1 second before clicking the next follow button
                finally:
                    t.sleep(1)

            # execute_script is used to scroll the window to the bottom of the page
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                       scroll_window)
            print(f'Followed {self.follows_count}')
            t.sleep(2)

    def quit(self):
        self.driver.quit()


bot = Instafollower()
bot.login()
bot.not_now()
bot.find_followers()
bot.follow()
bot.quit()
