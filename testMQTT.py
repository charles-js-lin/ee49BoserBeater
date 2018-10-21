from mqttclient import MQTTClient
from time import sleep
import random

#IOT ECLIPSE BROKER
#BROKER = "iot.eclipse.org"
#USER = None
#PWD = None

#HiveMQ Broker
BROKER = "broker.hivemq.com" #iot.eclipse.org
USER = None
PWD = None

print("Connecting to broker", BROKER, "...")
#sleep(2)
#CREATING the mqtt object and CONNECTING to the broker
mqtt = MQTTClient(BROKER, user=USER, password=PWD, ssl=False)

print("Connected!")

def mqtt_callback(topic,msg):
	print("RECEIVE topic = {}, msg = {}".format(topic,msg))

mqtt.set_callback(mqtt_callback)
mqtt.subscribe("charles/esp32/hi")

#PUBLISH - SUBSCRIBE LOOP
for i in range(5):
	#PUBLISHING a message
	topic = "charles/esp32/hi"
	message = "Hello " + str(random.randint(1,101))
	print("PUBLISH topic = {} message = {}".format(topic,message))
	mqtt.publish(topic, message)
	
	#CHECKING for a new message
	for _ in range(5):
		mqtt.check_msg()
		sleep(0.5) #pause for 0.5 second

#Close sockets
mqtt.disconnect()