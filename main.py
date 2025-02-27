from lib.websites_browsers.private_property import PPBrowser
from lib.websites_browsers.nigerian_property_center import NpcBrowser
import sys


if __name__ == '__main__':
    
    # sys.argv[0] is the script name
    print(f"Script name: {sys.argv[0]}")

    # Arguments passed to the script
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        website_arg = args[0]
        test_flag = len(args) == 2 and args[1] == '--test'
        
        if test_flag:
            print('Running in Test Mode!!!')

        website_browser_dict = {
            "pp" : PPBrowser,
            "npc": NpcBrowser
        }
        
        website_browser_dict.get(website_arg, 'pp')(test_mode=test_flag).scrape()
    else:
        print("No arguments provided.")
