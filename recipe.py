# -*- coding: utf-8 -*-



def remove_multiple_spaces(string):
    return(' '.join(string.split()))

class Recipe:
    def __init__(self, json):
       json_recipe = json
       self.url = json_recipe['url']
       self.title = json_recipe['recipe_title']
       self.ingredients = json_recipe['ingredients']
       self.steps = json_recipe['steps']
       self.normalize_title()
       self.normalize_steps()

    def __iter__(self):
        yield 'url', self.url
        yield 'title', self.title
        yield 'ingredients', self.ingredients
        yield 'steps', self.steps

    def normalize_title(self):
        self.title = self.title.strip()
            
    def normalize_steps(self):
        self.steps = [remove_multiple_spaces(step) for step in self.steps]         
        self.steps = [step for step in self.steps if step]

   
    
    def dump(self, filename):
        
        with open(filename, 'w') as f:
            json.dump(dict(self), f)

    def steps_to_string(self):
        return '\n\n'.join(self.steps)

    def ingredients_to_string(self):
        return '\n'.join([ingredient for ingredient in self.ingredients])

    def __str__(self):        
        steps_string = self.steps_to_string()
        return '\n\n'.join([self.url, self.title, self.ingredients_to_string(),  self.steps_to_string()])

if __name__ == '__main__':
    recipe = Recipe('data/eda_ru.json')
    recipe.dump('data/output.json')
    
    print(recipe)
