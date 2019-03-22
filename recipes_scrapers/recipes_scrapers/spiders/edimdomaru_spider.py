import scrapy
from recipes_scrapers.settings import SELECTORS

class EdimdomaRuSpider(scrapy.Spider):

    """ scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/126032-bystraya-fokachcha-s-tomatami-i-syrom" """

    name = "EdimdomaRu"

    def __init__(self, *args, **kwargs):
        super(EdimdomaRuSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
        

    def parse(self, response):

        yield {
            'url': response.request.url,
            'recipe_title': response.css(SELECTORS['recipe_title']).get(),
            'ingredients': self.parse_ingredients(response),
            'steps': response.css(SELECTORS['step']).getall()

        }

    def parse_ingredients(self, response):
        
        return [{'name': ingredient.css(SELECTORS['ingredient_name']).get(), 'amount': ingredient.css(SELECTORS['ingredient_amount']).get()} for ingredient in response.css(SELECTORS['ingredient'])]
