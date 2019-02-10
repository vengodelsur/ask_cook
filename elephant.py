# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

import json
import logging


app = Flask(__name__)
api = Api(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST', 'GET'])
def main_alice():
	if request.method == 'GET':
		return "Hello!\n"
	
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

		handle_dialog(request.json, response)

		logging.info('Response: %r', response)
		
		print(request.json['version'])
		return json.dumps(
			response,
			ensure_ascii=False,
			indent=2
		)

def handle_dialog(req, res):
	user_id = req['session']['user_id']

	if req['session']['new']:
		# Это новый пользователь.
		# Инициализируем сессию и поприветствуем его.

		sessionStorage[user_id] = {
			'suggests': [
				"Не хочу.",
				"Не буду.",
				"Отстань!",
			]
		}

		res['response']['text'] = 'Привет! Купи слона!'
		#res['response']['buttons'] = get_suggests(user_id)
		return

	# Обрабатываем ответ пользователя.
	if req['request']['original_utterance'].lower() in [
		'ладно',
		'куплю',
		'покупаю',
		'хорошо',
	]:
		# Пользователь согласился, прощаемся.
		res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
		return

	# Если нет, то убеждаем его купить слона!
	res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
		req['request']['original_utterance']
	)
	#res['response']['buttons'] = get_suggests(user_id)

if __name__ == "__main__":
	#app.run(debug=True)
        app.run(host='0.0.0.0', ssl_context='adhoc')
