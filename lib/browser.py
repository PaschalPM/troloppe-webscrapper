from selenium.webdriver.common.by import By
from seleniumbase import Driver


class Browser:
    browser, has_captcha =  None, False
    
    # Initialize the webdriver
    def __init__(self, has_captcha = False):
        self.has_captcha = has_captcha
        self.browser = Driver(uc=has_captcha, headless=False)
        
    def solve_captcha_page(self, url):
        if not self.has_captcha: 
            return
        
        self.open_page(url, True)
        
    
    def open_page(self, url: str, initial_load = False):
        if self.has_captcha and initial_load:
            self.browser.uc_open_with_reconnect(url, 6)
            self.browser.uc_gui_click_captcha()
        else:
            self.browser.open(url)
        
        
    def close_browser(self):
        self.browser.close()
    
    def quit(self):
        self.browser.quit()
        
        
    def add_input(self, by:By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        
        
    def click_button(self, by:By, value: str):
        button = self.browser.find_element(by=by, value=value)
        self.browser.execute_script("arguments[0].click();", button)
