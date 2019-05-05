intent_handlers = {}


def intent_handler(intent):
    def wrapper(function):
        intent_handlers[intent] = function
        return function
    return wrapper

utterances = {'hello': ['привет'],
              'help': ['помощь', 'что ты умеешь'],
              'fallback': ['проблемесы'],
              'search_recipe': ['как готовить шарлотку'],
              'start_cooking': ['начать'],
              'next_step': ['дальше'],
              'repeat_step': ['повтори'],
              'previous_step': ['назад'],
              'get_time': ['сколько минут'],
              'get_ingredient_amount': ['сколько яблок']}
suggests = {'hello': ['Привет! Назови блюдо, которое хочешь приготовить.'],
            'help': ['Ты можешь попросить меня найти рецепт, продиктовать его по шагам, переспросить продолжительность или уточнить количество ингредиента.'],
            'fallback': ['Я тебя не понимаю.'],
            'search_recipe': ['Вот рецепт.'],
            'start_cooking': ['Первый шаг.'],
            'next_step': ['Следующий шаг.'],
            'repeat_step': ['Повторяю.'],
            'previous_step': ['Возвращаюсь к предыдущему шагу.'],
            'get_time': ['20 минут.'],
            'get_ingredient_amount': ['Пять яблок.']}


@intent_handler('hello')
def handle_hello():
    return suggests['hello'][0]


@intent_handler('help')
def handle_help():
    return suggests['help'][0]


@intent_handler('fallback')
def handle_fallback():
    return suggests['fallback'][0]


@intent_handler('search_recipe')
def handle_search_recipe():
    return suggests['search_recipe'][0]


@intent_handler('start_cooking')
def handle_start_cooking():
    context.counter = 0
    return context.get_current_step()


@intent_handler('next_step')
def handle_next_step():
    context.counter += 1
    return context.get_current_step()

@intent_handler('repeat_step')
def handle_repeat_step():
    return context.get_current_step()


@intent_handler('previous_step')
def handle_previous_step():
    context.counter -= 1
    return context.get_current_step()

@intent_handler('get_time')
def handle_get_time():
    return suggests['get_time'][0]


@intent_handler('get_ingredient_amount')
def handle_get_ingredient_amount():
    return suggests['get_ingredient_amount'][0]

class Searcher:
    def __init__(self):
        self.api_key
        self.engine_id
        self.base_uri = 'https://www.googleapis.com/customsearch/v1?key=' + self.api_key + '&cx=' + self.engine_id + ':omuauf_lfve&q='
    def search(self, query):
        url = self.base_uri + query
class Context:

    def __init__(self):
        self.intent = 'fallback'
        self.counter = -1
        self.steps_mode = False
        self.steps = ['шаг ноль', 'шаг раз', 'шаг два']

    def set_recipe(self, recipe):
        self.recipe = recipe

    def get_current_step(self):
        return self.steps[self.counter]
    

class IntentClassifier:

    def __init__(self):
        self.intent = 'fallback'
        

    def predict(self, string):
        for key, value in utterances.items():
            if string in value:
                self.intent = key
        return intent_handlers[self.intent]()


clf = IntentClassifier()
context = Context()
print(clf.predict('начать'))
print(clf.predict('дальше'))
print(clf.predict('назад'))
print(clf.predict('дальше'))
print(clf.predict('повтори'))
