################################
# CONNECT TO INTERNET          #
################################

# Connect to the wifi network (EECS-PSK) and print IP address
# Advertise hostname on the network via mDNS
# Fetch and print internet time

# Establish Internet connection
from network import WLAN, STA_IF
from network import mDNS
import time

wlan = WLAN(STA_IF)
wlan.active(True)

#EECS-PSK, password: Thequickbrown
#Can test out with home network
#PC Hotspot: kennytan, kennytan
wlan.connect('kennytan', 'kennytan', 5000) 

for x in range(10):
    if not wlan.isconnected():
        print("Waiting for wlan connection")
        time.sleep(1)
    else:
        break

print("WiFi connected at", wlan.ifconfig()[0])

# Advertise as 'hostname', alternative to IP address
try:
    hostname = 'JoJo'
    mdns = mDNS(wlan)
    mdns.start(hostname, "MicroPython REPL")
    mdns.addService('_repl', '_tcp', 23, hostname)
    print("Advertised locally as {}.local".format(hostname))
except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

print("start telnet server")
telnet.start(user='micro', password='python') #dependent on microcontroller - use config

# fetch NTP time
from machine import RTC

print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 10
for _ in range(timeout):
    if rtc.synced():
        break
    print("Waiting for rtc time")
    time.sleep(1)

if rtc.synced():
    print(time.strftime("%c", time.localtime()))
    print("Connected to internet!")
else:
    print("could not get NTP time")

#in Shell49 can type 'ip' and it will tell us the IP address if it's connected. 
#else if returns 00000000 not connected