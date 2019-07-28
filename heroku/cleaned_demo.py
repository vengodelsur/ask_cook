# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
import pymemcache

import json
import logging
import os
from intents import *

app = Flask(__name__)
api = Api(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}





# Задаем параметры приложения Flask.

class Context:

    def __init__(self):
        self.intent = 'fallback'
        self.counter = -1
        self.steps_mode = False
        self.steps = ['Сливочное масло взбиваем на небольшой скорости с сахаром.', 'Постепенно добавляем 5 желтков и продолжаем взбивать.', 'Просеиваем муку к желтковой смеси.', 'Замешиваем тесто.',
'Сразу же отщипываем по кусочку теста и раскатываем. Делаем произвольной формы печенья.', 'Оставшийся желток смешиваем с молоком и смазываем с помощью кисточки поверхность всех печений. Смазывайте как можно гуще. Поверх этой глазури зубочисткой рисуем любые узоры.', 'Формочки выкладываем на противень с бумагой и выпекаем 10–15 минут в духовке при температуре 180 градусов.']
        self.ingredients = [{'name': 'Яичный желток', 'amount': '6 штук'},
                           {'name': 'Молоко', 'amount': '2 столовые ложки'},
                           {'name': 'Пшеничная мука', 'amount': '2 стакана'},
                           {'name': 'Сахар', 'amount': '1 стакан'},
                           {'name': 'Сливочное масло', 'amount': '200 граммов'}]
        self.ingredients_text = '.\n'.join([ingredient['name']+', ' + ingredient['amount'] for ingredient in self.ingredients])


    def set_recipe(self, recipe):
        self.recipe = recipe

    def get_current_step(self):
        if self.counter >= len(self.steps):
            return 'Готово!'
        if self.counter < 0:
            return 'Мы ещё не начали готовить'
        return self.steps[self.counter]
    



context = Context()

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

        
        clf = IntentClassifier()
        intent = clf.predict(request.json)
        intent_handlers[intent](request.json, response, context)
         

        logging.info('Response: %r', response)

        # print(request.json['version'])
        return json.dumps(
                response,
                ensure_ascii=False,
                indent=2
        )


@app.route("/memcached/<key>", methods=['POST', 'GET'])
def memcache_test(key):
    mc = pymemcache.Client(('cache', 11211))
    if request.method == 'POST':
        mc.set(key, request.get_data())
    return mc.get(key) or '[No value]'


if __name__ == "__main__":
    # app.run(debug=True)

    kwargs = {'ssl_context': 'adhoc'}
    if os.environ.get('NO_SSL'):
        # No ssl in docker
        assert 'ssl_context' in kwargs
        del kwargs['ssl_context']

    app.run(host='0.0.0.0', **kwargs)
