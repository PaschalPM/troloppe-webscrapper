from selenium.webdriver.common.by import By
from ...browser import Browser
from utils import tmp_store
from data_access import npc_query

class AgentProfileBrowser(Browser):
    AGENTS_PROFILE_TMP_STORE_KEY = 'agent_profile_url'
    CURRENT_PAGE_KEY = 'current_page'
    
    _total_num_pages = 560
    _base_url, test_mode = '', False

    
    def __init__(self, base_url, has_captcha=False, test_mode = False):
        self._base_url = base_url
        self.test_mode = test_mode
        super().__init__(has_captcha)
    

    def get_current_page_number(self):
        current_page = tmp_store.retrieve(self.CURRENT_PAGE_KEY)
        return current_page if current_page else 1 
        

    def goto_agents_page(self, page_number = 1, initial_load = False):
        url = f"{self._base_url}/agents?search=lagos&page={page_number}"
        self.open_page(url, initial_load)
    
    
    def scrape_and_cache_emails(self):
        # Return early if scraping is already completed
        if self.has_completed():
            return

        # Solve the captcha on the initial page to gain access
        self.solve_captcha_page(self._base_url)
        
        # Get the current page number to resume scraping from the correct point
        current_page_number = self.get_current_page_number()

        if 'Nigeria Property Centre' in self.browser.title:  

            for page_number in range(current_page_number, self._total_num_pages + 1): 
                self.goto_agents_page(page_number) 
                self.fetch_save_agent_c_websites(page_number) 
                print(f"Scrapped page {page_number} out of {self._total_num_pages}")

            
        print('Added ALL Agents Custom Emails to tmp store!!!')


    def fetch_save_agent_c_websites(self, page_number):
        # Find all property list elements on the current page
        property_list_elements = self.browser.find_elements(by=By.CLASS_NAME, value='property-list')
        
        # Iterate through each property listing
        for element in property_list_elements:
            try:
                # Check if the property has a link to an agent on 'estateagentsng.com'
                element.find_element(by=By.XPATH, value=".//a[contains(@href, 'estateagentsng.com')]")
                
                # Find the agent's profile link and add it to the email set
                agent_profile_element = element.find_element(by=By.XPATH, value=".//a[starts-with(@href, '/agents')]")
                custom_website = agent_profile_element.get_attribute('href')
                npc_query.insert_profile_url(custom_website)
                tmp_store.save(self.CURRENT_PAGE_KEY, page_number + 1, True)
            
            except:
                # If any error occurs (like missing elements), skip to the next iteration
                pass


    def has_completed(self):
        current_page_number = self.get_current_page_number()
        return current_page_number >= self._total_num_pages
    
    