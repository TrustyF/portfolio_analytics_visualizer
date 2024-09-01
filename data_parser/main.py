import json
from itertools import groupby
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

key_path = "creds/vue-portfolio-7361b-487cfbc9268b.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
client = bigquery.Client(credentials=credentials, project=credentials.project_id, )

QUERY = (
    "SELECT event_name,event_date,geo,event_params,user_id,user_properties,user_pseudo_id,event_params,event_timestamp,"
    "device"
    " FROM `vue-portfolio-7361b.analytics_452242460.events_*` "
    "WHERE event_date >= '20240813' "
    "AND event_name in ('router_nav','iframe_use','filter_use','nav_return_arrow','nav_up_arrow',"
    "'open_new_tab','page_leave')"
    "LIMIT 1000"
)

# API request
query_job = client.query(QUERY)

# convert
records = [dict(row) for row in query_job]
#
# with open('dumps/dump.json', 'w') as outfile:
#     json.dump(records, outfile, indent=1)

# with open('dumps/dump.json', 'r') as infile:
#     records = json.load(infile)

new_data = []
for event in records:
    new_data.append({
        'name': event['event_name'],
        'id': event['user_pseudo_id'],
        'geo': f"{event['geo']['country']}/{event['geo']['city']}",
        'device': f"{event['device']['category']}/{event['device']['mobile_brand_name']}/{event['device']['mobile_model_name']}",
        'date': event['event_date'],
        'timestamp': event['event_timestamp'],
        'value': [x['value']['string_value'] for x in event['event_params'] if x['key'] == 'info'][0],
    })

sorted_data = []

entry_index = 0
for date, events in groupby(new_data, key=lambda x: x['date']):
    sorted_data.append({
        'date': date,
        'users': {}
    })
    for user_id, value in groupby(events, key=lambda x: x['id']):

        all_val = list(sorted(value, key=lambda y: y['timestamp']))

        sorted_data[entry_index]['users'][user_id] = {}
        sorted_data[entry_index]['users'][user_id]['events'] = []
        sorted_data[entry_index]['users'][user_id]['geo'] = all_val[0]['geo']
        sorted_data[entry_index]['users'][user_id]['device'] = all_val[0]['device']

        for i, x in enumerate(all_val):
            temp = {
                'event_name': x['name'],
                'event_info': x['value'],
                'timestamp': x['timestamp'],
                'diff': 0
            }

            try:
                temp['diff'] = round((datetime.fromtimestamp(all_val[i + 1]['timestamp'] / 1000000)
                                      - datetime.fromtimestamp(x['timestamp'] / 1000000)).total_seconds(), 2)
            except Exception:
                temp['diff'] = 0.0

            sorted_data[entry_index]['users'][user_id]['events'].append(temp)
    entry_index += 1

sorted_data.sort(key=lambda x: x['date'],reverse=True)

with open('dumps/parsed_dump.json', 'w') as outfile:
    json.dump(sorted_data, outfile, indent=1)
