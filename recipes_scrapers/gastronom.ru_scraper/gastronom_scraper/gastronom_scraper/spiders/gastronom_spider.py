from gastronom_scraper.items import GastronomRecipe
import datetime
import scrapy
import json
import re


class GastronomSpider(scrapy.Spider):
	name = "gastronom-spider"
	start_urls = ["https://www.gastronom.ru/recipe/45817/pelmeni-sibirskie"]
	#start_urls = ["https://www.gastronom.ru/recipe/2118/falafel-iz-droblenogo-goroha"]
	#start_urls = ["https://www.gastronom.ru/recipe/4756/zakusochnyj-blinchatyj-tort"]
	
	def parse(self, response):
		title = response.css('[itemprop="name"]').xpath("text()").extract()[0]
		recipe_intro = self.parse_recipe_intro(response)
		ingredients = self.parse_ingredients(response)
		steps = self.parse_steps(response)
		add_info = self.parse_add_info(response)
		
		recipe_dict = {
			"title": title,
			"recipe_intro": recipe_intro,
			"ingredients": ingredients,
			"steps": steps,
			"add_info": add_info
		}
		
		with open("recipe.txt", "w") as outfile:
			json.dump(recipe_dict, outfile, ensure_ascii=False)
		
		return GastronomRecipe(
			title=title,
			recipe_intro=recipe_intro,
			ingredients=ingredients,
			steps=steps,
			add_info=add_info
		)
	
	def parse_ingredients(self, response):
		ing_sections = []
		for ing_sec in response.css('div.recipe__ingredient-title'):
			ing_sections.append(ing_sec)
		ing_sec_len = len(ing_sections)
		
		if ing_sec_len == 1:
			parent_section = ing_sections[0].xpath('parent::div')
			ing_list = parent_section.xpath('ul/li')
			partial_ingredients = self._get_ingredients(ing_list)
			ingredients_dict = { 'default': partial_ingredients }
			
			return ingredients_dict
		elif ing_sec_len > 1:
			resp = ing_sections[0].xpath('parent::div')
			
			ing_lists = resp.xpath('ul')
			ingredients_dict = {}
			for i, (ing_list, ing_section) in enumerate(zip(ing_lists, ing_sections)):
				ing_list = ing_list.xpath('li')
				if ing_list:
					if i == 0:
						ing_title = "default"
					else:
						ing_title = ing_section.xpath('text()').extract_first()
					
					partial_ingredients = self._get_ingredients(ing_list)
					ingredients_dict.update({ing_title: partial_ingredients})
			
			return ingredients_dict
		else:
			raise ValueError("Can't find Ingredients section")
	
	def _get_ingredients(self, ing_list):
		partial_ingredients = []
		for ing in ing_list:
			add_ing = []
			if ing.xpath('child::*'):
				add_ing = ing.xpath('child::*/text()').extract()
			partial_ingredients.append(add_ing + ing.xpath('text()').extract())
		return partial_ingredients
	
	def parse_steps(self, response):
		steps = []
		recipe_steps = response.css('[itemprop="recipeInstructions"]').css('div.recipe__step-text').xpath('text()')
		for i, step in enumerate(recipe_steps):
			step = step.extract()
			step = re.sub(r'\s+', ' ', step)
			steps.append(step)
		return steps
	
	def parse_add_info(self, response):
		add_info_titles = response.css('div.recipe__summary-list-title')
		add_info_descriptions = response.css('div.recipe__summary-list-des')
		
		add_info_dict = {}
		for info_title, info_description in zip(add_info_titles, add_info_descriptions):
			info_title = info_title.xpath('text()').extract()
			
			if info_title[0] == 'Источник':
				break
			
			if info_description.xpath('child::*'):
				info_description = info_description.xpath('child::*/text()').extract()
			else:
				info_description = info_description.xpath('text()').extract()
			
			add_info_dict.update({info_title[0]: info_description})
		
		return add_info_dict
	
	def parse_recipe_intro(self, response):
		intro = response.css('div.recipe__intro')
		if intro:
			intro = intro.xpath('p/text()').extract()
			return intro
		return []
