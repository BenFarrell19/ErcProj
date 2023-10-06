import datetime
import dateutil.parser
import json


data = json.load(open('clean quarterlies', 'r'))

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(d):
    return (d - epoch).total_seconds() * 1000.0


for dic in data:
    for key in dic:
        iso = dic[key]['released']
        dt = dateutil.parser.isoparse(iso)
        print(dt)

