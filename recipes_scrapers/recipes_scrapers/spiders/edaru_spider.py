import scrapy
from .base_spider import BaseSpider

class EdaRuSpider(BaseSpider):

    """ scrapy crawl EdaRu -a start_url="https://eda.ru/recepty/zakuski/brusketta-s-pomidorami-29566" """

    name = "EdaRu"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = 'eda.ru'

