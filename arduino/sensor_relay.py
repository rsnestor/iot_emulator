#!/usr/bin/python3

import requests
import json
import argparse
from sys import argv
from sensor_tmp36 import getTemp
from datetime import datetime

# ------------------------------------------------
# Simple IoT Relay Server 
# Expects sensor input from a serial port on 
# the runtime platform.
# 
# Version 0.1 beta (Prototype) - Expects serial
# input from a TMP36 analog sensor (Arduino) 
# ------------------------------------------------

ES_URL = ''

# Elasticsearch request parts 
headers = {
 'Content-Type': 'application/json',
 'Accept': 'text/plain, */*; q=0.01',
 'Accept-Encoding': 'gzip, deflate, br'
}
params = {}
proxies = {}
# request sensor template 
data = { 'location': '38.9586, -77.3570', 'ip': '75.106.133.2', 'propertyId': 12000, 'realtorId': 'URAWSM', 'city': 'Reston', 'state': 'VA', 'squareFootage': 50000, 'propertyType': 'Commercial', 'propertyIn': 'urban', 'temperature': getTemp(), 'humidity': 45, 'mold': 110, 'motion': 'Y', 'age': 22, 'timestamp': '' }


def relaySensorData(data,recs):
    if recs>0:
        for i in range(recs):
            relaySensorRecord(data)
    else:
        while(True):
            relaySensorRecord(data)


def relaySensorRecord(data):
    # datetime formatting 
    (dt, micro) = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    data['timestamp'] = "%s.%03d" % (dt, int(micro) / 1000)
    # read TMP36
    data['temperature'] = getTemp()

    #response = requests.post('https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/prop_mon_ix/_doc', data=json.dumps(data), auth=('elastic','<pwd>'), headers=headers)
    #response = requests.post('https://search-iottest-zrdh3oawbzm5a62ful33hnprbi.us-east-1.es.amazonaws.com/sensor-data/doc', data=json.dumps(data), headers=headers)
    response = requests.post(ES_URL, proxies=proxies, headers=headers, params=params, data=json.dumps(data))

    if response.status_code in (requests.codes.ok,requests.codes.created):
        if args.quiet != True:
            print("[{}] - OK\tRecord added: {} temp: {}".format(response.status_code,data['timestamp'],data['temperature']))
        if args.verbose:
            print(response.text)
    else:
        print("[{}] - ERROR\tRecord not added".format(response.status_code))
        response.raise_for_status()


# commandline argument definitions
parser = argparse.ArgumentParser(description="Start the sensor relay server")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-n", "--num_records", type=int, default=-1, help="number of records to relay")
parser.add_argument("-e", "--elastic_url", type=str, required=True, help='http(s)://<user>:<pwd>@elastichost>:<port>/<index>/<doc_type>')
parser.add_argument("-p", "--proxy_url", type=str, help="http(s)://<user>:<pwd>@<proxyhost>:<port>")
args = parser.parse_args()

# simplifying assignment - supports no_auth and basic_auth proxies 
if args.proxy_url:
    proxies['http'] = args.proxy_url
    proxies['https'] = args.proxy_url

ES_URL = args.elastic_url

relaySensorData(data,args.num_records)

