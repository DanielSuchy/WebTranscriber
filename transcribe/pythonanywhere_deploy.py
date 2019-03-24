from flask import Flask
from transcribe import bp

app = Flask(__name__)
app.register_blueprint(bp)
