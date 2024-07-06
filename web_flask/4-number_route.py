#!/usr/bin/python3
"""Write a script that starts a Flask web application
three routes, / , /hbnb, and /c/<text>"""
from flask import Flask
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


@app.route("/number/<n>", strict_slashes=False)
def hello_world_n(n):
    """adds the /number/<n> route, with sanitization"""
    if n.isnumeric():
        return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
