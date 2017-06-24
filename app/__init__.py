# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views
from app import upload
from app import upload1
from app import upload2
from app import upload3
from app import upload4
from app import upload5
from app import upload6
# Load the config file
app.config.from_object('config')