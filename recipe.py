# -*- coding: utf-8 -*-

import json

def remove_multiple_spaces(string):
    return(' '.join(string.split()))

class Recipe:
    def __init__(self, json_filename):
       with open(json_filename) as f:
           json_recipe = json.load(f)[0]
       self.url = json_recipe['url']
       self.title = json_recipe['recipe_title']
       self.ingredients = json_recipe['ingredients']
       self.steps = json_recipe['steps']
       self.normalize_steps()

    def __iter__(self):
        yield 'url', self.url
        yield 'title', self.title
        yield 'ingredients', self.ingredients
        yield 'steps', self.steps
            
    def normalize_steps(self):
        self.steps = [remove_multiple_spaces(step) for step in self.steps]         
        self.steps = [step for step in self.steps if step]
    
    def dump(self, filename):
        with open(filename, 'w') as f:
            json.dump(dict(self), f)

if __name__ == '__main__':
    recipe = Recipe('data/eda_ru.json')
    recipe.dump('data/output.json')
    print(recipe.steps)
