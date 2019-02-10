from OpenSSL import SSL
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')

def index():

    return 'Flask is running'



if __name__ == '__main__':
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('ssl.key')
    context.use_certificate_file('ssl.crt')

    app.run(host='127.0.0.1',port='12344',
        debug = False/True, ssl_context=context)
