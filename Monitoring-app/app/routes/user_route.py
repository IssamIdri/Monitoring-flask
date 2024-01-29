from flask import request, render_template, redirect, url_for, session, make_response
from app import app
from datetime import datetime
from app.data.mysql.create_db import DatabaseService

@app.route('/')
def login() -> any:
    return redirect(url_for('user_authentication'))

@app.route("/authentication", methods=["GET", "POST"])
def user_authentication() -> str:
    if request.method == "GET":
        return render_template("login.html")
    else:
        db_service = DatabaseService()
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = db_service.get_user_by_username_password(username, password)

        if user_data:
            print(user_data)
            # Store user_id in session
            session['user_id'] = user_data[1]

            # Set cookie for access time
            response = make_response(render_template('index.html'))
            response.set_cookie('access_time', str(datetime.now()))

            return response

        return render_template("login.html", error_message="Username or password not found")

@app.route("/log_out", methods=["GET"])
def log_out() -> str:
    # Clear session data and remove the access_time cookie
    session.clear()
    response = make_response(render_template("login.html"))
    response.delete_cookie('access_time')
    return response

