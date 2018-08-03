#!flask/bin/python
#encoding:utf-8
from app import app
import os
#print app.config["basedir"]
#print os.path.abspath(os.path.dirname(__file__))
app.run(host="0.0.0.0", debug=True, port=8080)