mport scrapy


class EdaSpider(scrapy.Spider):
    """ scrapy crawl eda -a start_url="https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566" """

    name = "eda"

    def __init__(self, *args, **kwargs):
        super(EdaSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        yield {
            'url': response.request.url,
            'recipe_title': response.css('body > div.wrapper-sel > section > section > div.recipe__title h1.recipe__name::text').get(),
            'ingredients': response.css('body > div.wrapper-sel > section > section > div.g-relative.js-responsive-banner-relative > div.ingredients-list.layout__content-col > div.ingredients-list__content p::attr(data-ingredient-object)').getall(),
            'steps': response.css('body > div.wrapper-sel > section > section > div.recipe__instruction > ul.recipe__steps li > div.instruction__wrap > span.instruction__description::text').getall()

        }

