from flask import Flask

app = Flask(__name__)

from brainComputer.gui.app import routes
