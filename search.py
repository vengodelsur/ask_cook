import requests

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'recipes_scrapers'))

from recipes_scrapers.spiders.edaru_spider import EdaRuSpider
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher

from recipe import Recipe

# more about running scrapy from script
# https://scrapy.readthedocs.io/en/latest/topics/practices.html



        





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
        
class RecipeSaver:
    def __init__(self):
        self.recipe = 'default'
    def set_recipe(self, spider):
        self.recipe = spider.result


searcher = Searcher()
link = searcher.search('печенье бретон')

data = RecipeSaver()
dispatcher.connect(data.set_recipe, signal=signals.spider_closed)

process = CrawlerProcess()
process.crawl(EdaRuSpider, start_url=link)
process.start()  


recipe = Recipe(data.recipe)
print(recipe.steps[3])


