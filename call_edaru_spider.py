import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'recipes_scrapers'))

from recipes_scrapers.spiders.edaru_spider import EdaRuSpider
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher

# more about running scrapy from script
# https://scrapy.readthedocs.io/en/latest/topics/practices.html


class RecipeSaver:
    def __init__(self):
        self.recipe = 'default'
    def set_recipe(self, spider):
        self.recipe = spider.result
        

data = RecipeSaver()
print(data.recipe)

dispatcher.connect(data.set_recipe, signal=signals.spider_closed)

process = CrawlerProcess()
process.crawl(EdaRuSpider, start_url='https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566')
process.start()  

print(data.recipe['steps'][3])

# we can get the crawling results into a variable using signals https://stackoverflow.com/questions/23574636/scrapy-from-script-output-in-json
# though it seems to conflict with the asynchronous nature of scrapy
# https://stackoverflow.com/questions/40237952/get-scrapy-crawler-output-results-in-script-file-function
