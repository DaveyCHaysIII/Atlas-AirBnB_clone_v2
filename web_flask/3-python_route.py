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


@app.route("/python/", defaults={'text', 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def hello_world_Python(text):
    """adds the /Python/<text> route, with sanitization"""
    formatted_text = escape(text).replace('_', ' ') if text else 'is cool'
    return f"Python {formatted_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
