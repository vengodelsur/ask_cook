from recipes_scrapers.items import Say7InfoRecipe
import datetime
import scrapy


class Say7InfoSpider(scrapy.Spider):
	name = "Say7Info"
	start_urls = ["https://www.say7.info/cook/recipe/958-Pechenochnyie-oladi.html"]
	
	def parse(self, response):
		title = response.css('[itemprop="name"]').xpath("text()").extract()[0]
		ingredients = self.parse_ingredients(response)
		steps = self.parse_steps(response)
		
		return Say7InfoRecipe(title=u"{}".format(title), ingredients=ingredients, steps=steps)
	
	
	def parse_steps(self, response):
		steps = []
		for i, step in enumerate(response.css('[id="stp"]').xpath("p/text()")):
			steps.append(step.extract())
		return steps
			
	
	def parse_ingredients(self, response):
		ingredients = []
		for i, ing in enumerate(response.css('div.c8:nth-child(5)').xpath("ul/li/text()")):
			ingredients.append(ing.extract())
		return ingredients
