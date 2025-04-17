from flask import Flask
from google.cloud import bigtable
from google.cloud.bigtable.row_filters import RowFilterChain, ValueRangeFilter

app = Flask(__name__)

client = bigtable.Client(admin=True)
instance = client.instance('ev-bigtable')
table = instance.table('ev-population')

@app.route('/rows')
def row_count():
    rows = table.read_rows()
    count = sum(1 for _ in rows)
    return str(count)

@app.route('/Best-BMW')
def best_bmw():
    rows = table.read_rows()
    count = 0
    for row in rows:
        make = row.cells.get('ev_info', {}).get(b'make', [])[0].value.decode('utf-8').lower()
        if make == 'bmw':
            try:
                erange = int(row.cells['ev_info'][b'electric range'][0].value.decode('utf-8'))
                if erange > 100:
                    count += 1
            except:
                continue
    return str(count)

@app.route('/tesla-owners')
def tesla_owners():
    rows = table.read_rows()
    count = 0
    for row in rows:
        try:
            make = row.cells['ev_info'][b'make'][0].value.decode('utf-8').lower()
            city = row.cells['ev_info'][b'city'][0].value.decode('utf-8').lower()
            if make == 'tesla' and city == 'seattle':
                count += 1
        except:
            continue
    return str(count)

@app.route('/update')
def update_range_
