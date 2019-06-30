
utterances = {'hello': ['алиса запусти навык спроси повара'],
              'help': ['помощь', 'что ты умеешь'],
              'fallback': ['проблемесы'],
              'search_recipe': ['как приготовить печенье бретон'],
              'start_cooking': ['начать готовить'],
              'next_step': ['дальше'],
              'repeat_step': ['повтори'],
              'previous_step': ['назад'],
              'get_time': ['сколько минут'],
              'get_ingredients': ['перечислить ингредиенты'],
              'get_ingredient_amount': ['алиса сколько яичных желтков']}

for key, value in utterances.items():
    utterances[key] = set(value[0].split())

responses = {'hello': ['Вы запустили навык “Спроси повара”. Что вы хотите приготовить?'],
            'help': ['Ты можешь попросить меня найти рецепт, продиктовать его по шагам, переспросить продолжительность или уточнить количество ингредиента.'],
            'fallback': ['Я тебя не понимаю.'],
            'search_recipe': ['Печенье «Бретон», время приготовления - 35 минут. Начать готовить или перечислить ингредиенты?'],
            'get_ingredients' : ['Яичный желток - 6 штук, Молоко - 2 столовые ложки, Пшеничная мука - 2 стакана, Сахар - 1 стакан, Сливочное масло - 200 г'],
            'get_time': ['20 минут.'],
            'get_ingredient_amount': ['Яичный желток - 6 штук. Начать готовить?']}

intent_handlers = {}


def intent_handler(intent):
    def wrapper(function):
        intent_handlers[intent] = function
        return function
    return wrapper




@intent_handler('hello')
def handle_hello(req, res, context):
    res['response']['text'] = responses['hello'][0]
    res['response']['tts'] = responses['hello'][0]

@intent_handler('help')
def handle_help(req, res, context):
    res['response']['text'] = responses['help'][0]
    res['response']['tts'] = responses['help'][0]


@intent_handler('fallback')
def handle_fallback(req, res, context):
    res['response']['text'] = responses['fallback'][0]
    res['response']['tts'] = responses['fallback'][0]


@intent_handler('search_recipe')
def handle_search_recipe(req, res, context):
    res['response']['text'] = responses['search_recipe'][0]
    res['response']['tts'] = responses['search_recipe'][0]


@intent_handler('start_cooking')
def handle_start_cooking(req, res, context):
    context.counter = 0
    res['response']['text'] = context.get_current_step()
    res['response']['tts'] = context.get_current_step()

@intent_handler('next_step')
def handle_next_step(req, res, context):
    context.counter += 1
    res['response']['text'] = context.get_current_step()
    res['response']['tts'] = context.get_current_step()
@intent_handler('repeat_step')
def handle_repeat_step(req, res, context):
    res['response']['text'] = context.get_current_step()
    res['response']['tts'] = context.get_current_step()

@intent_handler('previous_step')
def handle_previous_step(req, res, context):
    context.counter -= 1
    res['response']['text'] = context.get_current_step()

@intent_handler('get_ingredients')
def handle_get_ingredients(req, res, context):
    res['response']['text'] = context.ingredients_text
    res['response']['tts'] = context.ingredients_text

@intent_handler('get_time')
def handle_get_time(req, res, context):
    res['response']['text'] = responses['get_time'][0]
    res['response']['tts'] = responses['get_time'][0]
@intent_handler('get_ingredient_amount')
def handle_get_ingredient_amount(req, res, context):
    res['response']['text'] = responses['get_ingredient_amount'][0]
    res['response']['tts'] = responses['get_ingredient_amount'][0]

class IntentClassifier:

    def __init__(self):
        self.intent = 'fallback'
        
    def predict(self, req):
        if req['session']['new']:
            self.intent = 'hello'
            return self.intent
        #tokens = set(req['request']['nlu']['tokens'])
        tokens = set(req['request']['original_utterance'].lower().split())
        for key, value in utterances.items():
            print(tokens, value)
            if tokens <= value:
                
                self.intent = key
                return self.intent
        return self.intent

