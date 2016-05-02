from RESTClient import RESTClient, Services
from DbAccess import DbAccess

# Get last/todays rates
client = RESTClient(Services.ALL_RATES)
data = client.call_service()
db = DbAccess()

list = data.find('nsp:Cube', client.namespaces)

# Insert entries in DB
for entry in list:
    entry_date = entry.attrib['time']
    entry_date_id = db.insert_entry(entry_date)

    if entry_date_id == -1:
        entry_date_id = db.entry_get_id(entry_date)[0]

    # Insert rates in DB
    for rate in entry:
        db.insert_exchangeRate(
            entry_date_id, rate.attrib['currency'], 
            rate.attrib['rate']
        )