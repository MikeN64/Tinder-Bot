from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import random
import re
import requests
import config
import messages


class TinderBot():

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=config.CHROMEDRIVER_PATH)


    def _go_through_login_options(self):
        time.sleep(3)
        try:
            more_options_btn = self.driver.find_element_by_xpath('//button[text()="More Options"]')
            more_options_btn.click()
        except:
            print("More options not available")


    def _login_with_fb(self):
        time.sleep(3)
        try:
            email = config.EMAIL
            password = config.PASSWORD
            fb_btn = self.driver.find_element_by_xpath('//button//span[text()="Log in with Facebook"]//ancestor::button')
            fb_btn.click()

            time.sleep(3)
            base_window = self.driver.window_handles[0]
            popup = self.driver.window_handles[1]
            self.driver.switch_to.window(popup)
            email_input = self.driver.find_element_by_xpath('//input[@name="email"]')
            pass_input = self.driver.find_element_by_xpath('//input[@name="pass"]')
            login_btn = self.driver.find_element_by_xpath('//input[@name="login"]')
            email_input.send_keys(email)
            pass_input.send_keys(password)
            login_btn.click()
            self.driver.switch_to.window(base_window)
            time.sleep(3)

        except Exception:
            print("Error Logging in FB")


    def _click_btn(self, title):
        time.sleep(2)
        try:
            btn = self.driver.find_element_by_xpath('//span[text()="{}"]//ancestor::button'.format(title))
            btn.click()
        except:
            print("Clicking '{}' not working".format(title))


    def _swipe(self, title):
        swipe_btn = self.driver.find_element_by_xpath('//button[@aria-label="{}"]'.format(title))
        swipe_btn.click()


    def login(self):
        url = "https://www.tinder.com"
        self.driver.get(url)
        self._go_through_login_options()
        self._login_with_fb()


    def goto_swipe(self):
        self._click_btn("Allow")
        self._click_btn("Not interested")
        self._click_btn("I Accept")
        #self._click_btn("No Thanks")


    def swipe_like(self):
        return self._swipe("Like")


    def swipe_nope(self):
        return self._swipe("Nope")

    def auto_swipe(self):
        like_rate = config.LIKE_RATE
        like_margin = config.LIKE_RATE_MARGIN
        swipe_rate = config.SWIPE_RATE
        swipe_margin = config.SWIPE_RATE_MARGIN

        try:
            while True:
                like_chance = like_rate + random.uniform(-like_margin, like_margin)
                seconds = swipe_rate + random.uniform(-swipe_margin, swipe_margin)
                if random.random() <= like_chance:
                    self.swipe_like()
                else:
                    self.swipe_nope()
                time.sleep(seconds)
        except: 
            print("Interrupted")
            try:
                self.send_match_message()
                time.sleep(3)
                self.auto_swipe()
            except:
                print("Not a match interrupted")
                try:
                    self._click_btn("Not interested")
                    time.sleep(3)
                    self.auto_swipe()
                except:
                    print("Not a 'Not Interested' Interruption")


    def send_match_message(self):
        text_box = self.driver.find_element_by_xpath('//textarea[@placeholder="Say something nice!"]')
        text_box.send_keys("Hiya! How's your quarantine going?")


    def get_profile_pic_url(self):
        image_bg = self.driver.find_element_by_xpath("(//div[contains(@class, 'StretchedBox') and contains(@style,'background-image')])[last()]")
        style = image_bg.get_attribute("style")
        url = re.search("https://.*\.webp", style).group(0)
        print(url)


if __name__ == "__main__":
    bot = TinderBot()
    bot.login()
    bot.goto_swipe()
    bot.get_profile_pic_url()