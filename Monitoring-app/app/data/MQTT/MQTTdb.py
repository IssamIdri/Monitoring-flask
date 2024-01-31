from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class IOTDevice(db.Model) :
    
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    mac_address = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    luminosity = db.Column(db.Float)
    date = db.Column(db.DateTime)
    
   

    def __repr__(self) :
        return f'<IOTDevice {self.ip_address}>'
