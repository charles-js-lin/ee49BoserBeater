################################
# CONNECTING TO MQTT           #
################################
from mqttclient import MQTTClient
from time import sleep
import random

MAX_SPEED = 100

#IOT BROKER
BROKER = "broker.hivemq.com" #Alternatively, iot.eclipse.org
USER = None
PWD = None

print("Connecting to broker", BROKER, "...")

#CREATING the mqtt object and CONNECTING to the broker
mqtt = MQTTClient(BROKER, user=USER, password=PWD, ssl=False) #False for hivemq
topic = "charles/esp32/boserBeater"
mqtt.publish(topic, "BoserBeater is online :^)") #ESP32 IS PUBLISHING, CP RECEIVING
print("BoserBeater is online :^)")
currentSpeed = 0

def mqtt_callback(topic,msg):
    global currentSpeed

    message = msg.decode("utf-8") #msg comes in as byte-format, decode turns it directly into a string
    
    currentSpeed = int(round(float(message)))
    if currentSpeed>MAX_SPEED: #Capping it
        currentSpeed = MAX_SPEED

mqtt.set_callback(mqtt_callback)
mqtt.subscribe("charles/pc/boserBeater") #SUBSCRIBE TO COMPUTER TOPIC

################################
# SETUP                        #
################################

#Connect DRV V_in from Vusb. This is running on 5V
from machine import PWM, Pin, Timer
from board import A20, A21, A6, A14, A15
from time import sleep, ticks_ms
from max6675 import MAX6675

    ################################
    # THERMOCOUPLE                 #
    ################################
so = Pin(A14, mode=Pin.IN)
cs = Pin(A15, mode=Pin.OUT)
sck = Pin(A6, mode=Pin.OUT)
thermo = MAX6675(sck, cs, so)

    ################################
    # DC MOTOR                     #
    ################################
p20 = Pin(A20, mode=Pin.OUT)
p21 = Pin(A21, mode=Pin.OUT)

f = 100000
HI = 100
LO = 100 #MOTOR STARTS OFF NOT RUNNING

xIN1 = PWM(p20, freq = f, duty = HI)
xIN2 = PWM(p21, freq = f, duty = LO)

################################
# MAIN PROGRAM                 #
################################

mqtt.publish(topic, \
    "BoserBeater is now running." \
    "\r\r[INSTRUCTIONS]" \
    "\r -Input speed range: 0 - 100" \
    "\r -Starting speed = 0. Input a speed from 0 to 100." \
    "\r  Speeds 100 or greater will result in max speed." \
    "\r\r -Every 20 seconds, speed can be changed. " \
    "\r -Time elapsed and current temperature will also be displayed." \
    "\r\r -Input of '-1' will terminate the program!")

while True:
    mqtt.check_msg()
    if currentSpeed<0: #Terminate Program
        xIN2.duty(100)
        mqtt.publish(topic, "BoserBeater turning off.")
        mqtt.disconnect()
        break
    LO = MAX_SPEED-currentSpeed #msg is speed
    xIN2.duty(LO)
    temp = thermo.read()
    mqtt.publish(topic, \
        "[STATUS]" \
        "\r -Speed: " + str(currentSpeed) + "\r" \
        " -Current temperature: " + str(temp) + " C." \
        "\r -Time elapsed: " + str(int(ticks_ms()/1000)) + " s.")
    sleep(20)