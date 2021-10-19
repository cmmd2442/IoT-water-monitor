from umqtt.simple import MQTTClient
import network
import time
from sys import stdin, stdout
from machine import Pin

pin0 = Pin("D0", Pin.IN, Pin.PULL_UP)
pin1 = Pin("D1", Pin.IN, Pin.PULL_UP)


# AWS endpoint parameters.
HOST = b'a221o6x4vr797o-ats'    # ex: b'abcdefg1234567'
REGION = b'us-east-2'  # ex: b'us-east-1'

#CLIENT_ID = "xbee3"  # Should be unique for each device connected, text of your choice.
CLIENT_ID = "xbee5"  # Should be unique for each device connected, text of your choice.
AWS_ENDPOINT = b'%s.iot.%s.amazonaws.com' % (HOST, REGION)

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC = "sample/xbee"
MESSAGE = "AWS Sample Message 20210630"


def sub_cb(topic, msg):
    """
    Callback executed when messages from subscriptions are received. Prints
    the topic and the message.
    :param topic: Topic of the message.
    :param msg: Received message.
    """

    global msgs_received

    msgs_received += 1
    print("- Message received!")
    print("   * %s: %s" % (topic.decode("utf-8"), msg.decode("utf-8")))
    mess = msg.decode("utf-8")
    print("mess =  ")
    print(mess)

def subscribe_test(client_id=CLIENT_ID, hostname=AWS_ENDPOINT, sslp=SSL_PARAMS,
                   msg_limit=10):
    """
    Connects to AWS, subscribes to a topic and starts listening for messages.
    :param client_id: Unique identifier for the device connected.
    :param hostname: AWS hostname to connect to.
    :param sslp: SSL certificate parameters.
    :param msg_limit: Maximum number of messages to receive before
        disconnecting from AWS..
    """

    global msgs_received

    # Connect to AWS.
    client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
    client.set_callback(sub_cb)
    print("- Connecting to AWS... ", end="")
    client.connect()
    print("[OK]")
    # Subscribe to topic.
    print("- Subscribing to topic '%s'... " % TOPIC, end="")
    client.subscribe(TOPIC)
    print("[OK]")
    # Wait for messages.
    msgs_received = 0
    print('- Waiting for messages...')
    start=time.ticks_ms()
    while msgs_received < msg_limit:
        delta = time.ticks_diff(time.ticks_ms(), start)
        if(delta > 300000):
            break
        client.check_msg()
        time.sleep(1)
    # Disconnect.
    client.disconnect()
    print("- Done")


def publish_test(client_id=CLIENT_ID, hostname=AWS_ENDPOINT, sslp=SSL_PARAMS):
    """
    Connects to AWS, publishes a message and disconnects.
    :param client_id: Unique identifier for the device connected.
    :param hostname: AWS hostname to connect to.
    :param sslp: SSL certificate parameters.
    """

    # Connect to AWS.
    client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
    print("- Connecting to AWS... ", end="")
    client.connect()
    print("[OK]")
    # Publish message.
    print("- Publishing message... ", end="")
    client.publish(TOPIC, '{"message": "%s"}' % MESSAGE)
    print("[OK]")
    # Disconnect.
    client.disconnect()
    print("- Done")



print(" +---------------------------------------+")
print(" | XBee MicroPython AWS Subscribe Sample |")
print(" +---------------------------------------+\n")

msgs_received = 0
conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")


#MESSAGE = "CONNECTION ESTABLISHED"
#publish_test()


#data = stdin.read(500)
#print(data)


time.sleep(5)

while True:

	if(pin0.value() == 0):
            data = stdin.read(1100)
            print(data)
            time.sleep(5)
            MESSAGE = data
            publish_test()
            time.sleep(10)
            MESSAGE = ""
            data = ""
            print("test data")
            print(data)

	if(pin1.value() == 0):
		print("subscribe")
		subscribe_test()
	time.sleep(10)
