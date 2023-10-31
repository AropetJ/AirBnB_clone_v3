#!/usr/bin/python3
""" Starts a Flask Application """
from models import storage
from api.v1.views import app_views
import os
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
CORS(app, resources={'/*': {'origins': app_host}})
host = environ.get('HBNB_API_HOST')
port = environ.get('HBNB_API_PORT')


@app.teardown_appcontext
def close_db(error):
    """ Closes the Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    A handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """Runs the app on the commandline"""
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
