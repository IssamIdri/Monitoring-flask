from flask import request, render_template, redirect

from app.data.services.deviceservices import DeviceService
from app import app
from app.data.snmp_data.testsnmp import snmp_get

import re

@app.route('/snmp', methods=['GET', 'POST'])
def snmp_page():
    if request.method == 'POST':
        # Extract form data
        target = request.form.get('target')
        oid = request.form.get('oid')
        community = request.form.get('community', 'public')
        port = int(request.form.get('port', 161))

        # Perform SNMP GET request
        snmp_data = snmp_get(oid, target, community, port)

        # Extract numerical values using regular expression
        numeric_values = [float(match.group(1)) for match in re.finditer(r'INTEGER: (\d+)', str(snmp_data))]
        print(snmp_data)
        print(numeric_values)  # This will print a list of float values
        return render_template('snmp.html', snmp_data=snmp_data, numeric_values=numeric_values)
    else:
        # Render the SNMP form page
        return render_template('snmp.html', snmp_data=None)
