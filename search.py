import requests

class Searcher:
    def __init__(self):
        self.api_key = 'AIzaSyDjzp4FOOJxWupaC1buwavTUVTwRTXvXTw'
        self.engine_id = '013419476088701395201:z2hk7csm8es'
        self.base_uri = 'https://www.googleapis.com/customsearch/v1?key=' + self.api_key + '&cx=' + self.engine_id + '&q='
    def search(self, query):
        url = self.base_uri + query
        r = requests.get(url=url) 
        first_link = r.json()['items'][0]['link']
        return first_link
        
        

searcher = Searcher()
print(searcher.search('печенье бретон'))
