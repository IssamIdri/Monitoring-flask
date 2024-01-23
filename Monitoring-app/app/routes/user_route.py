from flask import request, render_template, redirect, url_for, session
from app import app


@app.route('/')
def login() -> any:
    return render_template("login.html",error_message = "Username or password not found")