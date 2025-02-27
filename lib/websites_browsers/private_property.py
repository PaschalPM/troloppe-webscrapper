from ..browser import Browser
from selenium.webdriver.common.by import By
from utils.convert_to_csv import convert_to_csv
import storage.credentials as credentials

class PPBrowser(Browser):

    _data = {}
    _total_num_pages = 209
    _base_url, test_mode = 'https://www.privateproperty.com.ng', False

    def __init__(self, has_captcha=False, test_mode = False):
        self.test_mode = test_mode
        super().__init__(has_captcha)
        
    def login(self, email: str, password: str):
        login_url = f"{self._base_url}/login"
        self.open_page(login_url)
        self.add_input(by=By.NAME, value='email', text=email)
        self.add_input(by=By.NAME, value='password', text=password)
        self.click_button(by=By.XPATH, value="//button[@type='submit' and contains(text(), 'Login Now')]")
        self.browser.implicitly_wait(5)


    def goto_property_requests(self, page_number = 0):
        url = f"{self._base_url}/profile/requests?state=5&type=&mode=&beds=&daterange=01%2F02%2F2022+-+18%2F02%2F2025&button=&page={page_number}"
        self.open_page(url)


    def extract_agent_contact_info(self):
        table_rows = self.browser.find_elements(By.XPATH, "//tr[.//span[contains(text(), 'Agent')]]")

        for row in table_rows:
            request_contact_node = row.find_element(by=By.XPATH, value=".//div[starts-with(@id, 'request-contact')]")
            self.browser.execute_script("arguments[0].style.display = 'block'", request_contact_node)
            lines = request_contact_node.text.split("\n")
            temp_data = {}
            
            for text in lines:
                if text.startswith(("Email", "Whatsapp", "Phone", "Name")):
                    entries = text.split(":", 1)
                    key = entries[0].strip().lower()
                    value = entries[1].strip().lower()
                    temp_data[key] = value
                    if key == 'name':
                        temp_data[key] = value.title()

            email = temp_data.get("email")
            
            if email:
                self._data[email] = temp_data


    def scrape_agent_contact_info(self):
        for page_num in range(self._total_num_pages):
            self.goto_property_requests(page_num)
            self.extract_agent_contact_info()
            print(f"Scrapped page {page_num + 1} out of {self._total_num_pages}")

    
    def get_data_list(self):
        return [value for _, value in self._data.items()]
    
    def scrape(self):
        self.login(credentials.EMAIL, credentials.PASSWORD)
        self.scrape_agent_contact_info()
        self.browser.quit()
        convert_to_csv(self.get_data_list(), 'private-property-agents.csv')