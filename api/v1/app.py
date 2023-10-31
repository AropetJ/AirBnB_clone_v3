#!/usr/bin/python3
""" A script that starts an API"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify, render_template, url_for
from models import storage
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.register_blueprint(app_views)

app.url_map.strict_slashes = False

port = os.getenv('HBNB_API_PORT', 5000)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')


@app.teardown_appcontext
def close_db(exception):
    """Closes the storage engine"""
    storage.close()


@app.errorhandler(Exception)
def error_handler(e):
    """Handles errors i.e the 404 page"""
    if isinstance(e, HTTPException):
        if type(e).__name__ == 'NotFound':
            e.description = 'Not found'
        response = {"error": e.description}
        error_code = e.code
    else:
        response = {"error": e}
        error_code = 500
    return make_response(jsonify(response), error_code)


if __name__ == "__main__":
    """Runs the app in the command line"""
    app.run(threade=True, host=host, port=port)
