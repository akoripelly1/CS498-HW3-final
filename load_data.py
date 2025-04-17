import csv
from google.cloud import bigtable
from google.cloud.bigtable.row import DirectRow

def safe_encode(value):
    return value.encode("utf-8") if isinstance(value, str) else str(value).encode("utf-8")

# Connect to Bigtable
client = bigtable.Client(admin=True)
instance = client.instance('ev-bigtable')
table = instance.table('ev-population')

# Open CSV file with correct encoding
with open('Electric_Vehicle_Population_Data.csv', 'r', encoding='latin1') as file:
    reader = csv.DictReader(file)

    print("CSV Columns:", reader.fieldnames)

    batch = []
    for i, row in enumerate(reader):
        row_key = safe_encode(row['DOL Vehicle ID'])

        bt_row = DirectRow(row_key=row_key, table=table)
        bt_row.set_cell('ev_info', 'make', safe_encode(row['Make']))
        bt_row.set_cell('ev_info', 'model', safe_encode(row['Model']))
        bt_row.set_cell('ev_info', 'model year', safe_encode(row['Model Year']))
        bt_row.set_cell('ev_info', 'electric range', safe_encode(row['Electric Range']))
        bt_row.set_cell('ev_info', 'city', safe_encode(row['City']))
        bt_row.set_cell('ev_info', 'county', safe_encode(row['County']))

        batch.append(bt_row)

        if len(batch) == 100:
            table.mutate_rows(batch)
            batch.clear()

    if batch:
        table.mutate_rows(batch)

print("✅ Data load complete.")

