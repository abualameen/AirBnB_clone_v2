#!/usr/bin/python3
"""
This script starts a Flask web application with three routes:
- Root (/): displays "Hello HBNB!"
- /hbnb: displays "HBNB"
- /c/<text>: displays "C " followed by the value of the text variable, replacing underscores with spaces
"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' when the root URL is accessed."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Display 'HBNB' when /hbnb URL is accessed."""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """Display 'C ' followed by the value of the text variable."""
    return 'C {}'.format(escape(text).replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)