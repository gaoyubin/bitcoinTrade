#!flask/bin/python
from app import app
import os
#print app.config["basedir"]
print os.path.abspath(os.path.dirname(__file__))
app.run(port=80)