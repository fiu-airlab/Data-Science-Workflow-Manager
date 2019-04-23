from flask import Flask
from dash import Dash
from flask_caching import Cache
import os

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
cache = Cache(app.server, config={'CACHE_TYPE': 'redis', 'CACHE_DEFAULT_TIMEOUT	': 3600})

from . import routes
