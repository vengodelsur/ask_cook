import scrapy
from recipes_scrapers.settings import SELECTORS

class BaseSpider(scrapy.Spider):


    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
        

    def parse(self, response):

        yield {
            'url': response.request.url,
            'recipe_title': response.css(SELECTORS[self.domain]['recipe_title']).get(),
            'ingredients': self.parse_ingredients(response),
            'steps': response.css(SELECTORS[self.domain]['step']).getall(),
            'add_info': self.parse_add_info(response) 

        }

    def parse_ingredients(self, response):
        return response.css(SELECTORS[self.domain]['ingredient']).getall()
        
