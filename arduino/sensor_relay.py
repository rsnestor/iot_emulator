#!/usr/bin/python3

from sensor_tmp36 import getTemp
import requests
import json
from datetime import datetime

headers = {
 'Content-Type': 'application/json',
 'Accept': 'text/plain, */*; q=0.01',
 'Accept-Encoding': 'gzip, deflate, br'
}

params = {
}

# request body
data = { 'location': '38.9586, -77.3570', 'ip': '75.106.133.2', 'propertyId': 12000, 'realtorId': 'URAWSM', 'city': 'Reston', 'state': 'VA', 'squareFootage': 50000, 'propertyType': 'Commercial', 'propertyIn': 'urban', 'temperature': getTemp(), 'humidity': 45, 'mold': 110, 'motion': 'Y', 'age': 22, 'timestamp': '' }

#datetime manipulation 
(dt, micro) = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
data['timestamp'] = "%s.%03d" % (dt, int(micro) / 1000)

#response = requests.post('https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/prop_mon_ix/_doc/888', data=json.dumps(data), auth=('elastic','<pwd>'), headers=headers)
response = requests.post('https://search-iottest-zrdh3oawbzm5a62ful33hnprbi.us-east-1.es.amazonaws.com/sensor-data/doc', data=json.dumps(data), headers=headers)

if response.status_code in (requests.codes.ok,requests.codes.created):
   print("[{}] - OK\tRecord added: {} temp: {}".format(response.status_code,data['timestamp'],data['temperature']))
else:
   print("[{}] - ERROR\tRecord not added".format(response.status_code))
   response.raise_for_status()

#print(response.text)
