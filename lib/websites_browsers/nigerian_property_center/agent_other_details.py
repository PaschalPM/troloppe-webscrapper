from ...browser import Browser
from data_access import npc_query
from utils import tmp_store
from selenium.webdriver.common.by import By

class AgentOtherDetailsBrowser(Browser):
    
    CURRENT_INDEX = 'current_index'
    
    _base_url, test_mode = '', False
    
    def __init__(self, base_url, has_captcha=False, test_mode = False):
        self._base_url = base_url
        self.test_mode = test_mode
        super().__init__(has_captcha)
        
    
    def get_current_idx(self):
        current_index = tmp_store.retrieve(self.CURRENT_INDEX)
        return current_index if current_index else 0

    def scrap_other_details(self):
        self.solve_captcha_page(self._base_url)
        current_idx = self.get_current_idx()
    
        npc_agents = npc_query.get_npc_agents(current_idx)
        total_agents = npc_query.get_total()
        
        for agent in npc_agents:
            self.open_page(agent['profile_url'])
            data = {}
            
            page_title = self.browser.find_element(by = By.CLASS_NAME, value = 'page-title')
            data['name'] = page_title.text
            
            panel_body = self.browser.find_element(by = By.CLASS_NAME, value = 'panel-body')
            extracted_details = panel_body.text.split('\n')
            
            for detail in extracted_details:
                if detail.startswith(("Address", "Phone", "Whatsapp", "Website")):
                    idx = extracted_details.index(detail)
                    if not detail.startswith("Website"):
                        data[detail.lower()] = extracted_details[idx + 1]
                    else:
                        c_website = extracted_details[idx + 1].strip()
                        try:
                            self.open_page(c_website)
                            a_element = self.browser.find_element(by=By.XPATH, value="//a[starts-with(@href, 'mailto:')]")
                            href = a_element.get_attribute('href')
                            _, email =  href.split(":")

                            if not email.strip():
                                email = None
                                
                            data['email'] = email.lower()
                        except:
                            pass
        
            self.update_and_track_agent(agent['id'], data)
            print(f"Scrapped {agent['id']}/{total_agents}")
    

    def update_and_track_agent(self, agent_id: int, data: dict):
        # agent_id serves as tracking id / CURRENT INDEX too
        
        if self.test_mode:       
            print(data)
            return
        
        npc_query.update_agent(agent_id, data)
        tmp_store.save(self.CURRENT_INDEX, agent_id, True)