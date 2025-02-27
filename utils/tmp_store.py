import json
import os

class TmpStore:
    
    file_path = 'storage/tmp.json'
    
    def get_store_data(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return {}
    
        try:  
            with open(self.file_path, 'r') as file:
                loaded_data = json.load(file)
                return loaded_data
        except FileNotFoundError:
            return {}


    def save(self, key: str, value, override = False):
    
        if self.retrieve(key) and not override:
            return

        store_data = self.get_store_data().copy()
        store_data[key] = value
        self.write_to_store(store_data)


    def delete(self, key: str):
        store_data = self.get_store_data()
        new_store_data = {k: v for k, v in store_data.items() if k != key}
        self.write_to_store(new_store_data)
    
        
    def retrieve(self, key: str):
        return self.get_store_data().get(key)


    def write_to_store(self, store_data):
        with open(self.file_path, 'w') as file:
            json.dump(store_data, file, indent=4)


    def flush(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print('Tmp Store flushed')
        else:
            print('No tmp store found')