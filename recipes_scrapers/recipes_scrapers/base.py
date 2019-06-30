# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

import json
import logging

steps = ['Поджарить хлеб на сухой сковородке или в духовке до золотистой корочки. В духовке это займет три-пять минут (в зависимости от размера ломтя хлеба) при температуре 200 градусов.',
         'Помидоры нарезать кубиками с ребром около полсантиметра. Мелко нарубить три зубчика чеснока.',
         'Разогреть сковороду, плеснуть в нее немного оливкового масла и высыпать в него помидоры и чеснок. Готовить их минуту-другую, просто чтобы прогреть, не потеряв вкуса свежего помидора. Тогда капнуть в сковороду бальзамического крема, перемешать и снять с огня.', 
         'Поджаренный хлеб пропитать оставшимся оливковым маслом, разлив понемногу на каждый ломоть. Сверху выложить теплые помидоры, посолить по вкусу, посыпать свежемолотым черным перцем и мелко нарезанной зеленью — любой, какая окажется под рукой. И подавать как закуску — например, к вину.']
app = Flask(__name__)
api = Api(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST', 'GET'])
def main_alice():
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

		handle_dialog(request.json, response,steps)

		logging.info('Response: %r', response)
		
		#print(request.json['version'])
		return json.dumps(
			response,
			ensure_ascii=False,
			indent=2
		)

def handle_dialog(req, res,steps):
	user_id = req['session']['user_id']

	if req['session']['new']:
		# Это новый пользователь.
		# Инициализируем сессию и поприветствуем его.

		res['response']['text'] = 'Привет! Это рецепты. Какое блюдо готовим?'
    # Обрабатываем ответ пользователя.
	  if req['request']['original_utterance'].lower() in ['бутерброд',]:
      stepss(req=req,res=res, steps=steps)
		return

