from app import app
import foodstuffs
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html") 
