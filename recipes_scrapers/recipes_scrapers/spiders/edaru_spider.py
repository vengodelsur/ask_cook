import scrapy


class EdaRuSpider(scrapy.Spider):

    """ scrapy crawl eda -a start_url="https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566" """

    name = "EdaRu"

    def __init__(self, *args, **kwargs):
        super(EdaRuSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):

        selectors = {'recipe_title': 'h1.recipe__name::text',
                     'ingredient': 'p::attr(data-ingredient-object)',
                     'step': 'span.instruction__description::text'}
        yield {
            'url': response.request.url,
            'recipe_title': response.css(selectors['recipe_title']).get(),
            'ingredients': response.css(selectors['ingredient']).getall(),
            'steps': response.css(selectors['step']).getall()

        }
