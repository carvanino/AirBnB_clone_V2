#!/usr//bin/python3
"""
Gets all state and render as a list
"""

from flask import Flask
from flask import render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def remove_session(self):
    storage.close()


@app.route('/states_list')
def state_list():
    states = storage.all('State')
    print(states)
    return render_template('7-states_list.html', states=states)

"""
@app.teardown_appcontext
def remove_session(self):
    storage.close()
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
