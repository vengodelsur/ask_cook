import scrapy
from .base_spider import BaseSpider

class Say7InfoSpider(BaseSpider):

    """ scrapy crawl Say7Info -a start_url="https://www.say7.info/cook/recipe/958-Pechenochnyie-oladi.html" """

    name = "Say7Info"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = 'say7.info'


    
