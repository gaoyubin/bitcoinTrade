#!/usr/bin/env python3
from app import app
import os
#print app.config["basedir"]
#print os.path.abspath(os.path.dirname(__file__))
app.run(host="127.0.0.1", debug=True, port=8080)
