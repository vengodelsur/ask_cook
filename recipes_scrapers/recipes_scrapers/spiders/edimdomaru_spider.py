import scrapy
from .base_spider import BaseSpider
from recipes_scrapers.settings import SELECTORS


class EdimdomaRuSpider(BaseSpider):

    """ scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/126032-bystraya-fokachcha-s-tomatami-i-syrom" """

    name = "EdimdomaRu"

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)


        self.start_urls = [kwargs.get('start_url')]
        self.domain = 'edimdoma.ru'

    def parse_ingredients(self, response):
        return [{'name': ingredient.css(SELECTORS[self.domain]['ingredient_name']).get(), 'amount': ingredient.css(SELECTORS[self.domain]['ingredient_amount']).get()} for ingredient in response.css(SELECTORS[self.domain]['ingredient'])]
