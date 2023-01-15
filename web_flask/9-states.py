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
    """ Closes the sqlalchemy session """

    storage.close()


@app.route('/states')
def states():
    """ Renders the 9-states.html page for all states"""

    states = storage.all('State')
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def states_id(id):
    """ Renders the 9-states.html page for a specific state """

    for key, value in storage.all('State').items():
        if value.id == id:
            return render_template('9-states.html', states=value)
    return render_template('9-states.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
