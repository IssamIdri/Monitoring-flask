#from app.data.snmp_data.load_data_by_snmp_info import LoadDataBySnmpInfo
from config import DEBUG, HOST
from app import app

if __name__ == '__main__':
    #LoadDataBySnmpInfo().start()
    app.run(debug=DEBUG, host=HOST)
