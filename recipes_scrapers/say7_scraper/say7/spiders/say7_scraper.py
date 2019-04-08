from say7.items import Say7Recipe
import datetime
import scrapy
import json
import re


class Say7Spider(scrapy.Spider):
	name = "say7-spider"
	start_urls = ["https://www.say7.info/cook/recipe/935-Pelmeni.html"]
	# start_urls = ["https://www.say7.info/cook/recipe/1301-Pesochnyie-kolca.html"]
	
	
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
		
		with open("recipe.txt", "w", encoding = 'utf-8') as outfile:
			json.dump(recipe_dict, outfile, ensure_ascii=False)
		
		return Say7Recipe(
			title=title,
			recipe_intro=recipe_intro,
			ingredients=ingredients,
			steps=steps,
			add_info=add_info
		)
	

	def parse_ingredients(self, response):
		ing_sections = []
		for ing_sec in response.css('h3'):
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
			ingredient = add_ing + ing.xpath('text()').extract()
			ingredient_dict = {"name": [], "amount": [], "text": ingredient}
			partial_ingredients.append(ingredient_dict)
		return partial_ingredients
	
	def parse_steps(self, response):
		steps = []
		recipe_steps = response.css('[itemprop="recipeInstructions"]').css('div.stepbystep.e-instructions').xpath('p/text()')
		for i, step in enumerate(recipe_steps):
			step = step.extract()
			steps.append(step)
		return steps
	 
        
	def parse_add_info(self, response):
		return {}
	
	def parse_recipe_intro(self, response):
		intro = response.css('[itemprop="description"]').xpath("text()").extract()
		intro[-1] = response.css('[itemprop="recipeYield"]').xpath("text()").extract()[0] #  сколько можно приготовить с помощью этого рецепта
		if intro != '':
			return intro 
		return []
