from flask import Flask
from app.data.mysql.create_db import DatabaseService
from config import SECRET_KEY

# creating databases and tables
DatabaseService()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

from app.routes.snmp import snmp_page
from app.routes import user_route
from app.routes import showdevices
from app.routes.adddevice import adddevice
from app.routes.updatedevice import update_device
from app.routes.deletedevice import delete_device
from app.routes.graphedevice import showgraphedevice
from app.routes.index import index
