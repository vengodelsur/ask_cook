from gastronom_scraper.items import GastronomRecipe
import datetime
import scrapy
import json


class GastronomSpider(scrapy.Spider):
	name = "gastronom-spider"
	start_urls = ["https://www.gastronom.ru/recipe/45817/pelmeni-sibirskie"]
	#start_urls = ["https://www.gastronom.ru/recipe/2118/falafel-iz-droblenogo-goroha"]
	
	def parse(self, response):
		title = response.css('[itemprop="name"]').xpath("text()").extract()[0]
		#print("title: ", title)
		ingredients = self.parse_ingredients(response)
		#print("ingredients: ", ingredients)
		steps = self.parse_steps(response)
		#print("steps: ", steps)
		
		recipe_dict = { "title": title, "ingredients": ingredients, "steps": steps }
		with open("recipe.txt", "w") as outfile:
			json.dump(recipe_dict, outfile, ensure_ascii=False)
		
		return GastronomRecipe(title=title, ingredients=ingredients, steps=steps)
	
	def parse_ingredients(self, response):
		ing_sections = []
		for ing_sec in response.css('div.recipe__ingredient-title'):
			ing_sections.append(ing_sec)
		ing_sec_len = len(ing_sections)
		if ing_sec_len == 1:
			print("one ing section")
			parent_section = ing_sections[0].xpath('parent::div')
			ing_list = parent_section.xpath('ul')
			partial_ingredients = self._get_ingredients(ing_list)
			return partial_ingredients
		elif ing_sec_len > 1:
			ing_sections.pop(0)
			resp = response.css('main').xpath('div[2]/section/div[6]/div[1]')
			ingredients_dict = {}
			for i, ing_sec in enumerate(ing_sections):
				ing_list = resp.xpath(''.join(['ul[', str(2+i), ']']))
				ing_title = ing_sec.xpath('text()').extract_first()
				partial_ingredients = self._get_ingredients(ing_list)
				ingredients_dict.update({ing_title: partial_ingredients})
			return [ingredients_dict]
		else:
			raise ValueError("Can't find Ingredients section")
	
	def _get_ingredients(self, ing_list):
		partial_ingredients = []
		for ing in ing_list.xpath('li'):
			add_ing = []
			if ing.xpath('child::*'):
				add_ing = ing.xpath('child::*/text()').extract()
			partial_ingredients.append(add_ing + ing.xpath('text()').extract())
		return partial_ingredients
	
	def parse_steps(self, response):
		steps = []
		recipe_steps = response.css('[itemprop="recipeInstructions"]').css('div.recipe__step-text').xpath('text()')
		for i, step in enumerate(recipe_steps):
			steps.append(step.extract())
		return steps
