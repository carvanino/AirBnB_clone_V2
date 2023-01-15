#!/usr/bin/python3
"""
HBNB filters Module
"""


from flask import Flask
from flask import render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def remove_session(self):
    """ Closes the sqlalchemy session """

    storage.close()


@app.route('/hbnb_filters')
def hbnb():
    """ Renders the 10-hbnb_filters.html """

    states = storage.all('State')
    # cities = storage.all('City')
    amenities = storage.all('Amenity')
    return render_template(
            '10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
