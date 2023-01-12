#!/usr/bin/python3
"""
Starts a web application using a variable and specifying a default
for path based the variage
"""

from flask import Flask
from markupsafe import escape
app = Flask(__name__)

app.url_map.strict_slashes = False


@app.route('/')
def hello_Hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def use_var(text):
    # text = text.replace("_", " ")
    return f'C {escape(text)}'


@app.route('/python/')
@app.route('/python/<text>')
def use_existing_var(text='is cool'):
    return f'Python {escape(text)}'


@app.route('/number/<int:n>')
def use_var_int(n):
    if type(n) == int:
        return f'{escape(n)} is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
