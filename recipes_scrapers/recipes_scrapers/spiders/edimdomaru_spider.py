import scrapy
from .base_spider import BaseSpider
from recipes_scrapers.settings import SELECTORS


class EdimdomaRuSpider(BaseSpider):

    """ scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/126032-bystraya-fokachcha-s-tomatami-i-syrom" 
        scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/6426-pelmeni"
    """

    name = "EdimdomaRu"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = 'edimdoma.ru'

    def parse_ingredients(self, response):
        sections = response.css(SELECTORS[self.domain]['ingredient_section'])
        ingredients = {}

        for section in sections:
            section_name = section.css(SELECTORS[self.domain]['ingredient_section_name']).get()
            ing_list = section.css(SELECTORS[self.domain]['ingredient'])
            ingredients[section_name] = self._get_ingredients(ing_list)
        return ingredients

    def _get_ingredients(self, ing_list):
        return [{'name': ingredient.css(SELECTORS[self.domain]['ingredient_name']).get(), 'amount': ingredient.css(SELECTORS[self.domain]['ingredient_amount']).get()} for ingredient in ing_list]
