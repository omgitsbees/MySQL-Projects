from flask import Flask, request, render_template, redirect, url_for
from google.cloud import bigquery
import os

app = Flask(__name__)

# Set up Google Cloud BigQuery client
os.environ ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/kyleh/Visual Studio Code/Python/hospital_app/omgitsbeesdata-977f7c98796d.json"
client = bigquery.Client(project="omgitsbeesdata")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    ssn = request.form['ssn']
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    insurance_id = request.form['insurance_id']
    pcp = request.form['pcp']

    table_id = "omgitsbeesdata.Hospital_DB.Patients"
    rows_to_insert = [
        {u"ssn": int(ssn), u"name": name, u"address": address, u"phone": phone, u"insurance_id": int(insurance_id), u"pcp": int(pcp)},
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        return redirect(url_for('index'))
    else:
        return f'Encountered errors while inserting rows: {errors}'
    
if __name__ == '__main__':
    app.run(debug=True)