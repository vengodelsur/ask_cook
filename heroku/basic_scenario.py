# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

import json
import logging
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
        self.steps = [
    'Поджарить хлеб на сухой сковородке или в духовке до золотистой корочки. В духовке это займет три-пять минут (в зависимости от размера ломтя хлеба) при температуре 200 градусов.', 'Помидоры нарезать кубиками с ребром около полсантиметра. Мелко нарубить три зубчика чеснока.', 'Разогреть сковороду, плеснуть в нее немного оливкового масла и высыпать в него помидоры и чеснок. Готовить их минуту-другую, просто чтобы прогреть, не потеряв вкуса свежего помидора. Тогда капнуть в сковороду бальзамического крема, перемешать и снять с огня.',
                                                                                                                       'Поджаренный хлеб пропитать оставшимся оливковым маслом, разлив понемногу на каждый ломоть. Сверху выложить теплые помидоры, посолить по вкусу, посыпать свежемолотым черным перцем и мелко нарезанной зеленью — любой, какая окажется под рукой. И подавать как закуску — например, к вину.']

    def set_recipe(self, recipe):
        self.recipe = recipe

    def get_current_step(self):
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




if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', ssl_context='adhoc')
