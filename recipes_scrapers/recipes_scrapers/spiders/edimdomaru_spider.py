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

    def parse_add_info(self, response):
        time = response.css(SELECTORS[self.domain]['add_info_time'])
        nutritional_value_container = response.css(SELECTORS[self.domain]['add_info_nutritional_value']) 
        return {'Время готовки': [time.css('span::text').get(), time.xpath('text()').extract()[0]],
                'Количество порций': response.css(SELECTORS[self.domain]['add_info_servings']).get(),
                'Описание': response.css(SELECTORS[self.domain]['add_info_description']).get(),
                'Пищевая ценность': self._get_nutritional_value(nutritional_value_container)}

    def _get_nutritional_value(self, container):
        kkal = container.css('div.kkal-meter')
        nutrition = {'Калории' : kkal.css('div.kkal-meter__value::text').get(), 'Единицы' : kkal.css('div.kkal-meter__unit::text').get(), 'Проценты' : kkal.css('div.kkal-meter__percent::text').get()}
        parts = container.css('div.nutritional-value__nutritional-list')
        
        for part in parts.css('tr.definition-list-table__tr'):
            
            key = part.css('td.definition-list-table__td::text')
            value = part.css('td.definition-list-table__td_value::text').get()
            nutrition[key.get()] = value
          
        return nutrition
        

    def _get_ingredients(self, ing_list):
        return [{'name': ingredient.css(SELECTORS[self.domain]['ingredient_name']).get(), 'amount': ingredient.css(SELECTORS[self.domain]['ingredient_amount']).get()} for ingredient in ing_list]
