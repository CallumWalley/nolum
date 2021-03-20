from flask import Flask
import os
import re
import csv
import json
import urllib.request
import hashlib

app = Flask(__name__)


@app.route('/bullshit')
def hello():
    return re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)


