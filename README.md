# Property Monitoring Kit (IoT)
  An IoT client/server emulator using Elixir - Innovation Day 08/2018
---
### MVP0 
- [ ] Raspberry Pi wireless integration with SensorPush or other "real" sensor - *(team)*

### MVP1 
- [ ] Free public IoT sensors and/or sensor data - *Sagar*
- [x] Elixir client/server foundation code.  Connectivity via lightweight sockets - *Scott/Kashi*
- [x] FNM 2017 10K Stats on REO and MF properties (number of properties/units, UPB book value, vacancy stats, REO repair expenses, etc.) - *Tim*
- [x] ELK Dashboard - *Scott*
- [x] Mock sensor data generator - *Tim/Kashi* 

### MVP2 (with additional bandwidth)
- [ ] Relay server code expansion. Log and forward sensor data to a *sink* server (aggregator).  
- [ ] Sink server file I/O (for Logstash)
- [x] Performance test with Elixir server (request throughput)
- [x] The "Property Management Kit" design (1 slide), with estimated cost 
- [x] Commercially available sensors vs. Raspberry Pi customized (cost comparison)

### MVP3
- [ ] Potential integration applicability and/or utilization of cloud IoT solutions (AWS, Google, or Azure)

---
**Raspbian GUI config/startup**  
`sudo raspi-config`  

**Manual "Sanity" Test (client/server)**  
`iex -S mix`  
`[iex]Relay.start(7878) //any available port`  
`[bash]telnet localhost 7878 //enter characters then exit (^C)`  

*Note: telnet has been removed from OS X, use `nc -t -c localhost 7878`

**Testing the Relay Server**  
`mix test --exclude external:true`  

**Load testing a remote Relay Server**  
On the remote machine (e.g., 'raspberrypi3'), start the server:  
`[iex]Relay.start(9999) //this is the test default port`  

Ensure the context settings are correct in the RelayTest (test/perf_test.exs):  
`  setup_all do  
    {:ok, rhost: '<remote_hostname>',  
          load1: 100,  
          load_max: 1000  
    }  
  end`  

`mix test --only external:true`  

**ElasticSearch (cloud)**  
`curl -x http://<userid>:<pwd>@zsproxy.fanniemae.com:9480 -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix -XPUT -H "Content-Type: application/json" -d '{ "mappings": {"reo": { "properties": { "location": { "type": "geo_point" } } } } }'`

`curl -x http://<userid>:<pwd>@zsproxy.fanniemae.com:9480 -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix/reo -XPOST -H "Content-Type: application/json" -d '{"propertyId": "14703", "realtorId": "DG024", "city": "Gilbert", "state": "AZ", "location": "33.3528, -111.7890", "squareFootage": "5000+", "propertyType": "MF", "propertyIn": "rural", "temperature": "50", "humidity": "86", "mold": "100", "motion(vacant)": "N"}'`

`curl -x http://<userid>:<pwd>@zsproxy.fanniemae.com:9480 -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix/reo/_search?pretty=true`  

**Kibana**  
https://2e826f4a17fe4d268864822c643da6d3.us-east-1.aws.found.io:9243/app/kibana#/discover  
  
**Arduino Sketch**  
https://create.arduino.cc/editor/rsnestor/eac61b40-c205-4a41-ad43-aa9db20f8e8a/preview - Sketch (code) editor  
  
**Reference**    
https://elixir-lang.org/getting-started - Elixir language docs  
https://hex.pm/ - Elixir Hex (dependency repo)  
https://github.com/elixir-ecto/ecto - Database support for Elixir  
https://github.com/securing/gattacker - BLE Sniffer  
https://thingspeak.com/ - IOT Private Cloud Aggregator  
https://devpost.com/software/sensorpush  
https://stackoverflow.com/questions/437061/how-do-you-monitor-network-traffic-on-the-iphone  
https://github.com/highmobility/bluetooth-websocket-server  
https://robots.thoughtbot.com/playing-with-sockets-and-processes-in-elixir  
https://fred.stlouisfed.org/series/RRVRUSQ156N  

**Retail Monitoring**  
https://ring.com
