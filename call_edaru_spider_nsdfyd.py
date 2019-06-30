import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'recipes_scrapers'))

from recipes_scrapers.spiders.edaru_spider import EdaRuSpider
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher

from natasha import MoneyRangeExtractor
from recipe import remove_multiple_spaces


class RecipeSaver:
    def __init__(self):
        self.recipe = 'default'
    def set_recipe(self, spider):
        self.recipe = spider.result

def normalize_steps(text):
    steps = text.split('\n')
    steps = [remove_multiple_spaces(step) for step in steps]
    steps = [step for step in steps if step]
    return ' '.join(steps)




# more about running scrapy from script
# https://scrapy.readthedocs.io/en/latest/topics/practices.html

data = RecipeSaver()
dispatcher.connect(data.set_recipe, signal=signals.spider_closed)

start_url='https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566'
process = CrawlerProcess()
process.crawl(EdaRuSpider, start_url=start_url)
process.start()  

# dict_keys(['steps', 'add_info', 'url', 'ingredients', 'recipe_title'])

text = ''.join(data.recipe['steps'])
text = text.replace('три', '3')
text = text.replace('пять', '5')
text = normalize_steps(text)
print('RECIPE TEXT')
print(text)

print('MATCHES')

extractor = MoneyRangeExtractor()
matches = extractor(text)

for match in matches:
    start, stop = match.span
    print(start, stop, text[start:stop])

# FoodExtractor
"""
Extracts ingredients, intermediate products, and the
final dish in cooking.
"""
# ToolExtractor
"""
Extracts objects such as cookwares, jars, bottles, and knives
are tools.
"""
# DurationExtractor
"""
Extracts expressions to denote duration of a cooking action, such as
heating time. This includes numbers and units.
"""
# ChefActionExtractor
"""
Extracts expressions to specify the quantity of foods. They are mainly number expressions followed by units.
"""
# FoodActionExtractor
"""
Extracts actions taken by the chef.
"""
# ToolStateExtractor
"""
Extracts actions taken by food.
"""
# FoodStateExtractor
"""
Extracts expression describing taste, color, etc
"""

# we can get the crawling results into a variable using signals https://stackoverflow.com/questions/23574636/scrapy-from-script-output-in-json
# though it seems to conflict with the asynchronous nature of scrapy
# https://stackoverflow.com/questions/40237952/get-scrapy-crawler-output-results-in-script-file-function
