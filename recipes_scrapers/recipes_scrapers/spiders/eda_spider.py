import scrapy

class IngredientsSpider(scrapy.Spider):
    name = "ingredients"

    start_urls = [
            'https://eda.ru/recepty/supy/sirnij-sup-po-francuzski-s-kuricej-32614',
            'https://eda.ru/recepty/osnovnye-blyuda/kurica-v-kislo-sladkom-souse-po-kitajski-14456',
        ]

    def parse(self, response):
        yield {
            'url': response.request.url,
            'recipe_title': response.css('body > div.wrapper-sel > section > section > div.recipe__title h1.recipe__name::text').get(),
            'ingredients': response.css('body > div.wrapper-sel > section > section > div.g-relative.js-responsive-banner-relative > div.ingredients-list.layout__content-col > div.ingredients-list__content p::attr(data-ingredient-object)').getall()
        }
