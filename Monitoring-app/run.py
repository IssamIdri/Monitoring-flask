from app.data.snmp_data.regitredatasnmp import LoadDataBySnmpInfo

from config import DEBUG, HOST
from app import app


if __name__ == '__main__':
    LoadDataBySnmpInfo().start()
    #TemperatureReceiver("iot/esisa/test").connect()
    app.run(debug=DEBUG, host=HOST)
