#!/usr/bin/python3
"""
Gets all states and all city with a specific route id
"""


from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
states = storage.all('State')


@app.teardown_appcontext
def session_remove(self):
    storage.close()


@app.route('/states')
def states():
    states = storage.all('State')
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def states_id(id):
    for key, value in storage.all('State').items():
        if value.id == id:
            print("yes\n")
            print(value)
            return render_template('9-states.html', states=value)
        else:
            return render_template('9-states.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
