import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'recipes_scrapers'))

from recipes_scrapers.spiders.eda_spider import EdaSpider
from scrapy.crawler import CrawlerProcess

# more about running scrapy from script
# https://scrapy.readthedocs.io/en/latest/topics/practices.html

DATA_DIR = 'data/'

process = CrawlerProcess({'FEED_FORMAT': 'json',
                         'FEED_URI': DATA_DIR + 'eda_ru.json'})

process.crawl(
    EdaSpider, start_url='https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566')
process.start()

# we can get the crawling results into a variable using signals https://stackoverflow.com/questions/23574636/scrapy-from-script-output-in-json
# though it seems to conflict with the asynchronous nature of scrapy
# https://stackoverflow.com/questions/40237952/get-scrapy-crawler-output-results-in-script-file-function
