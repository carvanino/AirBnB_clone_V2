#!/usr/bin/python3
"""
Start Flask web application with two routes
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_Hbnb():
    """ Displays Hello HBNB """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """ Displays HBNB """
    return 'HBNB'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
