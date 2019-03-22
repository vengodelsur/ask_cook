import scrapy


class EdimdomaRuSpider(scrapy.Spider):

    """ scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/126032-bystraya-fokachcha-s-tomatami-i-syrom" """

    name = "EdimdomaRu"

    def __init__(self, *args, **kwargs):
        super(EdimdomaRuSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
        self.selectors = {'recipe_title': 'h1.recipe-header__name::text',
                          'ingredient_name': 'span.recipe_ingredient_title::text',
                          'ingredient_amount': 'td.definition-list-table__td.definition-list-table__td_value::text',
                          'ingredient': 'div.field-row.recipe_ingredients  table.definition-list-table',
                          'step': 'div.plain-text.recipe_step_text::text'}

    def parse(self, response):

        yield {
            'url': response.request.url,
            'recipe_title': response.css(self.selectors['recipe_title']).get(),
            'ingredients': self.parse_ingredients(response),
            'steps': response.css(self.selectors['step']).getall()

        }

    def parse_ingredients(self, response):
        return [{'name': ingredient.css(self.selectors['ingredient_name']).get(), 'amount': ingredient.css(self.selectors['ingredient_amount']).get()} for ingredient in response.css(self.selectors['ingredient'])]
