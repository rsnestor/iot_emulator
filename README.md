# Property Management Kit (IoT)
  An IoT client/server emulator using Elixir
---
### MVP0 
- Raspberry Pi wireless integration with SensorPush or other "real" sensor - *(team)*

### MVP1 
- Free public
- IoT sensors and/or sensor data - *Sagar*
- Elixir client/server code.  Connectivity via lightweight sockets - *Scott/Kashi*
- FNM 2017 10K Stats on REO and MF properties (number of properties/units, UPB book value, vacancy stats, REO repair expenses, etc.) - *Tim*
- ELK Dashboard - *Scott*
- Mock sensor data generator - *Tim* 

### MVP2 (with additional bandwidth)
- Elixir server code enhancement. Log and forward sensor data.  Socket connection (local) and forward over http. 
- Performance test with Elixir server (request throughput)
- The "Property Management Kit" design (1 slide), with estimated cost 
- Commercially available sensors vs. Raspberry Pi customized 

### MVP3
- Potential integration applicability and/or utilization of cloud IoT solutions (AWS, Google, or Azure)

---
**Raspbian GUI config/startup**
`sudo raspi-config`

**Manual "Sanity" Test (client/server)**
`mix compile`
`iex -S mix`
`[iex]IotEmulator.start(7878) //any available port`

`[bash]telnet localhost 7878 //enter characters then exit (^C)`

*Note: telnet has been removed from OS X, use `nc -t -c localhost 7878`


**Reference**

https://hex.pm/ - Elixir Hex (dependency repo)

https://thingspeak.com/ - IOT Private Cloud Aggregator

https://devpost.com/software/sensorpush

https://stackoverflow.com/questions/437061/how-do-you-monitor-network-traffic-on-the-iphone

https://github.com/highmobility/bluetooth-websocket-server

https://robots.thoughtbot.com/playing-with-sockets-and-processes-in-elixir
