from RESTClient import RESTClient, Services
from DbAccess import DbAccess

# Get last/todays rates
client = RESTClient(Services.TODAYS_RATES)
data = client.call_service()
db = DbAccess()

# Get item
item = data.find('nsp:Cube', client.namespaces)

# Insert entry in DB
today = item.__getitem__(0).attrib['time']
today_id = db.insert_entry(today)

if today_id == -1:
    today_id = db.entry_get_id(today)[0]

# Insert rates in DB
for rate in item.find('nsp:Cube', client.namespaces):
    db.insert_exchangeRate(
        today_id, rate.attrib['currency'], 
        rate.attrib['rate']
    )