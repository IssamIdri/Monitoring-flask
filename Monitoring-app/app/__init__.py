from flask import Flask
from app.data.mysql.create_db import CreateDatabase
from config import SECRET_KEY

# creating databases and tables
CreateDatabase()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


from app.routes import user_route
