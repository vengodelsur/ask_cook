from recipes_scrapers.items import Say7InfoRecipe
import datetime
import scrapy


class Say7InfoSpider(scrapy.Spider):
    name = "Say7Info"
    start_urls = [
        "https://www.say7.info/cook/recipe/958-Pechenochnyie-oladi.html"]

    def parse(self, response):
        title = response.css('[itemprop="name"]::text').get()
        ingredients = self.parse_ingredients(response)
        steps = self.parse_steps(response)

        return Say7InfoRecipe(title=u"{}".format(title), ingredients=ingredients, steps=steps)

    def parse_steps(self, response):
        steps = response.css('[itemprop="recipeInstructions"] p::text').getall()
        return steps

    def parse_ingredients(self, response):
        ingredients = response.css('[itemprop="recipeIngredient"]::text').getall()
        return ingredients
