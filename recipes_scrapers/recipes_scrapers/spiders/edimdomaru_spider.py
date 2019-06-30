import scrapy
from .base_spider import BaseSpider
from recipes_scrapers.settings import SELECTORS


class EdimdomaRuSpider(BaseSpider):

    """ scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/126032-bystraya-fokachcha-s-tomatami-i-syrom" 
        scrapy crawl EdimdomaRu -a start_url="https://www.edimdoma.ru/retsepty/6426-pelmeni"
    """

    name = "EdimdomaRu"
    domain = 'edimdoma.ru'
    selectors = SELECTORS[domain]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_page(self, respose):
        # follow links to recipe pages
        for href in response.css('article.card + a::attr(href)'):
            yield response.follow(href, self.parse_recipe)

        # follow pagination links
        for href in response.css('a.paginator__nav.paginator__nav_next::attr(href)'):
            yield response.follow(href, self.parse_page)

        

    def parse_ingredients(self, response):
        sections = response.css(self.selectors['ingredient_section'])
        ingredients = {}

        for section in sections:
            section_name = section.css(self.selectors['ingredient_section_name']).get()
            ing_list = section.css(self.selectors['ingredient'])
            ingredients[section_name] = self._get_ingredients(ing_list)
        return ingredients

    def parse_add_info(self, response):
        time = response.css(self.selectors['add_info_time'])
        nutritional_value_container = response.css(self.selectors['add_info_nutritional_value']) 
        
             
        return {'Время готовки': self._get_time(time),
                'Количество порций': response.css(self.selectors['add_info_servings']).get(),
                'Описание': response.css(self.selectors['add_info_description']).get(),
                'Пищевая ценность': self._get_nutritional_value(nutritional_value_container)}

    def _get_time(self, time):
        parts = time.css('span::text').getall()
        time_list = []
        for i in range(len(parts)):
            time_list.append(parts[i])
            time_list.append(time.xpath('text()').extract()[i])
        return time_list

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
        return [{'name': ingredient.css(self.selectors['ingredient_name']).get(), 'amount': ingredient.css(self.selectors['ingredient_amount']).get()} for ingredient in ing_list]
