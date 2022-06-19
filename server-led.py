# Main template for our paho.mqtt.client code import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from gpiozero import LED
import paho.mqtt.client as mqtt
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setwarnings(False)


led = LED(20)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flg,  rc):
	print("Connected with result code "+str(rc))
	
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("listen")
	client.connected_flag = True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

	if str (msg.payload) == "b'on'":
		led.on()
		GPIO.output(20, GPIO.HIGH)
	if str (msg.payload) == "b'off'":
		led.off()
		GPIO.output(20, GPIO.LOW)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60) # localhost is the Raspberry Pi itself

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
