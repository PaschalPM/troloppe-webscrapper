from .agent_profile import AgentProfileBrowser
from .agent_other_details import AgentOtherDetailsBrowser
from utils.convert_to_csv import convert_to_csv
from data_access import npc_query

class NpcBrowser():
    agent_c_websites_browser, agent_other_details_browser = None, None
    _base_url = 'https://nigeriapropertycentre.com'
    
    def __init__(self, has_captcha=True, test_mode = False):
        self.agent_c_websites_browser = AgentProfileBrowser(self._base_url, has_captcha, test_mode)
        self.agent_other_details_browser = AgentOtherDetailsBrowser(self._base_url, has_captcha, test_mode)
    
    
    def scrape(self):
        self.agent_c_websites_browser.scrape_and_cache_emails()
        self.agent_c_websites_browser.quit()
        self.agent_other_details_browser.scrap_other_details()
        self.agent_other_details_browser.quit()
        convert_to_csv(npc_query.get_npc_agents(), 'npc-agents.csv')
        