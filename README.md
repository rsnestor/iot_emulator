# Property Monitoring Kit (IoT)
An IoT relay "reference implementation" to gather metrics from the local environment and forward that data to a centralized data repository for analysis and inquiry.  Code and other artifacts in this repo were originally created as a client/server IoT *emulator* for a corporate Innovation Day (08/2018).  It has since evolved into a working, fully integrated prototype (for temperature).  
  
After grabbing 1st place at the August Innovation Day, this idea has received some additional interest.  The architecture has subsequently evolved from a wireless socket server implemented in Elixir, to an integrated Relay server written in Python.  The relay runs on Raspberry Pi (3rd gen), gathers sensor data from Arduino (MKR1000) on the serial COM port (USB) and forwards it to Elasticsearch.  
  
In general, this has been a fun project that combined various programming languages, operating platforms (Pi), and a little bit of electronics (i.e., reading an analog temperature sensor TMP36).  One potential "use case" for this technology would be the passive monitoring of a large portfolio of (mostly vacant) REO properties.  Here's a quick video that explains it => https://youtu.be/zMzwnkWBwMs
  
---
Now for the tech stack ... Although the Raspberry Pi can be configured in either console or desktop mode, it still requires peripherals to interact with the desktop unless you've installed a virtual networking server (preferably one that doesn't drain all the hardware resources).  Fortunately there is a "light" VNCServer distribution that does the trick.  There's a link in the Reference section below if you'd like more details on installing VNC on the Raspberry Pi.  
  
**Raspbian GUI config/startup**  
`sudo raspi-config`  - To toggle your Pi between console and desktop modes  
  
**Arduino and Python**  
The new relay server is written in Python and reads the ambient temperature from a sensor connected to the Raspberry Pi's USB port.  

https://create.arduino.cc/editor/rsnestor/eac61b40-c205-4a41-ad43-aa9db20f8e8a/preview - Sketch (code) editor.  The "sketch" package contains an image of the Arduino board wiring and the code that translates the TMP36 miniVolt output to Celsius and Fahrenheit.  The translated TMP36 temperature is sent along with other mock data to Elasticsearch apx. every 5 seconds (adjustable within the code).  
`python3 -c 'import sensor_tmp36 as s; s.testHarness()'` - Verify that the temp sensor can be read from the COM USB port  
`python3 ./sensor_relay.py` - Begin reading the temp and relaying to ES  

**Elixir**
Although the Elixir socket server code is currently dormant, it still works and can be launched and tested in the following ways:  

**Manual "Sanity" Test (client/server)**  
`iex -S mix`  
`[iex]Relay.start(7878) //any available port`  
`[bash]telnet localhost 7878 //enter characters then exit (^C)`*  

*Note: telnet has been removed from OS X, use `nc -t -c localhost 7878`

**Executing the Socket Server Unit tests**  
`mix test --exclude external:true`  

**Load testing a remote Relay Server**  
On the remote machine (e.g., 'raspberrypi3'), start the server:  
`[iex]Relay.start(9999) //this is the test default port`  

Modify the RelayTest performance test with the correct host and desired load (test/perf_test.exs):  
`  setup_all do  
    {:ok, rhost: '<remote_hostname>',  
          load1: 100,  
          load_max: 1000  
    }  
  end`  

`mix test --only external:true`  
  
---
The following cheatsheet is intended for connectivity checking of the relay platform (Raspberry Pi) with an external Elasticsearch domain (destination *sink*).  The following includes proxy directives for connectivity from a secure network (i.e., behind a corporate firewall).  The following AWS Elasticsearch URLs are no longer active, but left for clarity.  

**ElasticSearch (cloud)**  
The following PUT call will designate the "location" field as a `geo_point` data type so it can be aggregated for geographic (map) visualizations in Kibana.  Note:  This only works for new/empty indexes!  Note 2:  The index in this case is `iot_prop_mon_ix` and `reo` is the document type.  See Elasticsearch documentation for more detail (references below).  
`curl -x http://<userid>:<pwd>@<proxyhost>:<port> -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix -XPUT -H "Content-Type: application/json" -d '{ "mappings": {"reo": { "properties": { "location": { "type": "geo_point" } } } } }'`

The following POST creates a single document record.  
`curl -x http://<userid>:<pwd>@<proxyhost>:<port> -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix/reo -XPOST -H "Content-Type: application/json" -d '{"propertyId": "14703", "realtorId": "DG024", "city": "Gilbert", "state": "AZ", "location": "33.3528, -111.7890", "squareFootage": "5000+", "propertyType": "MF", "propertyIn": "rural", "temperature": "50", "humidity": "86", "mold": "100", "motion(vacant)": "N"}'`

The following "dumps" all the documents (in human readable format) from the remote index to stdout ... use with caution :-P   
`curl -x http://<userid>:<pwd>@<proxyhost>:<port> -u elastic:<ec_pwd> https://60b12664d5504516b7cb5a20862cbf19.us-east-1.aws.found.io:9243/iot_prop_mon_ix/reo/_search?pretty=true`  

**Kibana**  
https://2e826f4a17fe4d268864822c643da6d3.us-east-1.aws.found.io:9243/app/kibana#/discover    

---
Our original Innovation Day Check List (prioritized):  
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
**Reference**   
https://www.elastic.co/ - Elasticsearch doc (ES rocks!)
https://www.realvnc.com/en/connect/docs/raspberry-pi.html - VNC on the Pi  
https://elixir-lang.org/getting-started - Elixir language docs  
https://hex.pm/ - Elixir Hex (dependency repo)  
https://robots.thoughtbot.com/playing-with-sockets-and-processes-in-elixir - The foundation for our Elixir relay  
https://fred.stlouisfed.org/series/RRVRUSQ156N - U.S. rental vacancy rates (another use case)  
  
https://github.com/elixir-ecto/ecto - Database support for Elixir (not used here)  
https://github.com/securing/gattacker - BLE Sniffer for Elixir (cool, but haven't tried it yet)  
https://thingspeak.com/ - IOT Private Cloud Aggregator (alternative cloud solution)  
https://devpost.com/software/sensorpush - I use this at home, it's great!)  
https://stackoverflow.com/questions/437061/how-do-you-monitor-network-traffic-on-the-iphone - Interesting thread  
https://github.com/highmobility/bluetooth-websocket-server  

http://www.fanniemae.com/resources/file/ir/pdf/quarterly-annual-results/2017/10k_2017.pdf - Fannie Mae 2017 10K
http://www.freddiemac.com/investors/financials/pdf/10k_021518.pdf - Freddie Mac 2017 10K

**Retail Monitoring and Home Security**  
https://ring.com - A leading manufacturer of consumer HD security cameras.  Remote mobile connectivity and cloud data storage.  
