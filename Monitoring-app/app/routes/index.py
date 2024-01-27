from flask import request, render_template
from app import app



@app.route('/index')
def index():
    return render_template('index.html')