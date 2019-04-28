# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

import json
import logging


app = Flask(__name__)
api = Api(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

steps = [
    'Поджарить хлеб на сухой сковородке или в духовке до золотистой корочки. В духовке это займет три-пять минут (в зависимости от размера ломтя хлеба) при температуре 200 градусов.', 'Помидоры нарезать кубиками с ребром около полсантиметра. Мелко нарубить три зубчика чеснока.', 'Разогреть сковороду, плеснуть в нее немного оливкового масла и высыпать в него помидоры и чеснок. Готовить их минуту-другую, просто чтобы прогреть, не потеряв вкуса свежего помидора. Тогда капнуть в сковороду бальзамического крема, перемешать и снять с огня.',
                                                                                                                       'Поджаренный хлеб пропитать оставшимся оливковым маслом, разлив понемногу на каждый ломоть. Сверху выложить теплые помидоры, посолить по вкусу, посыпать свежемолотым черным перцем и мелко нарезанной зеленью — любой, какая окажется под рукой. И подавать как закуску — например, к вину.']

# Задаем параметры приложения Flask.

context = {'step_counter': -1, 'show_recipe': False}


@app.route("/", methods=['POST', 'GET'])
def main_alice():
    req = request.json

    if request.method == 'GET':
        return jsonify("Hello!\n")

    if request.method == 'POST':
    # Функция получает тело запроса и возвращает ответ.

        logging.info('Request: %r', request.json)

        response = {
            "version": request.json['version'],
                "session": request.json['session'],
                "response": {
                    "end_session": False
                }
        }

        user_id = req['session']['user_id']

        if req['session']['new']:
            # Это новый пользователь.
            handle_hello(request.json, response, context)

        if req['request']['original_utterance'].lower() in ['брускетта', 'бутерброд']:
            handle_show_recipe(request.json, response, context)

        if req['request']['original_utterance'].lower() in ['начать']:
            context['step_counter'] = 0
            context['show_recipe'] = True
            handle_show_step(request.json, response, context)

        if req['request']['original_utterance'].lower() in ['дальше']:
            if context['show_recipe']:
                context['step_counter'] += 1
            handle_show_step(request.json, response, context)

        logging.info('Response: %r', response)

        # print(request.json['version'])
        return json.dumps(
                response,
                ensure_ascii=False,
                indent=2
        )


def handle_hello(req, res, context):

    # Инициализируем сессию и поприветствуем его.
    print(context)
    res['response']['text'] = 'Привет! Что готовим?'
    context['step_counter'] = -1
    return


def handle_show_recipe(req, res, context):
    print(context)
    res['response'][
        'text'] = 'Здесь типа описание, можно ингредиенты глянуть. Начать готовить?'
    context['step_counter'] = -1
    return


def handle_show_step(req, res, context):
    print(context)
    if context['show_recipe']:

        i = context['step_counter']
        if i < 0:
            res['response']['text'] = 'чо дальше-то, еще не готовим ничего'
            return
        if i >= len(steps):
            res['response']['text'] = 'рецепт в с ё'
            return

        res['response']['text'] = steps[i]
        return
    else:
        res['response']['text'] = 'чо дальше-то, еще не готовим ничего'
        return


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', ssl_context='adhoc')

