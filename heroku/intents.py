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

intent_handlers = {}


def intent_handler(intent):
    def wrapper(function):
        intent_handlers[intent] = function
        return function
    return wrapper




@intent_handler('hello')
def handle_hello(req, res, context):
    res['response']['text'] = ['hello'][0]


@intent_handler('help')
def handle_help(req, res, context):
    res['response']['text'] = suggests['help'][0]


@intent_handler('fallback')
def handle_fallback(req, res, context):
    res['response']['text'] = ['fallback'][0]


@intent_handler('search_recipe')
def handle_search_recipe(req, res, context):
    res['response']['text'] = ['search_recipe'][0]


@intent_handler('start_cooking')
def handle_start_cooking(req, res, context):
    context.counter = 0
    res['response']['text'] = context.get_current_step()


@intent_handler('next_step')
def handle_next_step(req, res, context):
    context.counter += 1
    res['response']['text'] = context.get_current_step()

@intent_handler('repeat_step')
def handle_repeat_step(req, res, context):
    res['response']['text'] = context.get_current_step()


@intent_handler('previous_step')
def handle_previous_step(req, res, context):
    context.counter -= 1
    res['response']['text'] = context.get_current_step()

@intent_handler('get_time')
def handle_get_time(req, res, context):
    res['response']['text'] = suggests['get_time'][0]


@intent_handler('get_ingredient_amount')
def handle_get_ingredient_amount(req, res, context):
    res['response']['text'] = suggests['get_ingredient_amount'][0]


class IntentClassifier:

    def __init__(self):
        self.intent = 'fallback'
        

    def predict(self, req):
        if req['session']['new']:
            self.intent = 'hello'
            return self.intent
        string = req['request']['original_utterance']
        for key, value in utterances.items():
            if string in value:
                self.intent = key
        return self.intent

