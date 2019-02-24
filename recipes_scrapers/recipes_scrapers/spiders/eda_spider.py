import scrapy


class EdaSpider(scrapy.Spider):
    """ scrapy crawl eda -a start_url="https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566" """

    name = "eda"

    def __init__(self, *args, **kwargs):
        super(EdaSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        yield {
            'url': response.request.url,
            'recipe_title': response.css('div.recipe__title h1.recipe__name::text').get(),
            'ingredients': response.css('div.ingredients-list__content p::attr(data-ingredient-object)').getall(),
            'steps': response.css('ul.recipe__steps li > div.instruction__wrap > span.instruction__description::text').getall()

        }

