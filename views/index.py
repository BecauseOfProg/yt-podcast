from flask import render_template
from app import app
from g import DOMAIN


@app.route("/")
def home():
    '''Homepage of youtube-podcast'''
    return render_template('index.html', DOMAIN=DOMAIN)
