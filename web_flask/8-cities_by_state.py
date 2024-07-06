#!/usr/bin/python3
"""Write a script that starts a Flask web application
three routes, / , /hbnb, and /c/<text>"""
from models import storage
from models.state import State
from models.city import City
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """adds the / route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hello_world_hbnb():
    """adds the /hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def hello_world_c(text):
    """adds the /c/<text> route, with sanitization"""
    formatted_text = escape(text).replace('_', ' ')
    return f"C {formatted_text}"


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def hello_world_Python(text='is cool'):
    """adds the /Python/<text> route, with sanitization"""
    formatted_text = escape(text).replace('_', ' ')
    return f"Python {formatted_text}"


@app.route("/number/<int:n>", strict_slashes=False)
def hello_world_n(n):
    """adds the /number/<n> route, with sanitization"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def hello_world_number_template(n):
    """adds the /number_template/<n> route, with sanitization"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def hello_world_number_odd_or_even(n):
    """adds the /number_odd_or_even/<n> route, with sanitization"""
    if n % 2 == 0:
        value = 'even'
    else:
        value = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, value=value)


@app.teardown_appcontext
def teardown_db(exception):
    """removes the current session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def render_states():
    """renders states from db to route /states_list """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.route("/cities_by_states", strict_slashes=False)
def render_cities_by_state():
    """renders cities and states from db to route /cities_by_state"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
