import paho.mqtt.client as paho                         # mqtt library
import os
import json
import time
import random
from datetime import datetime

'''
#######################################
BEGIN THE THINGS NETWORK
Variables to interact with TTN
'''

# Communication with TheThingsNetwork
ttn_host = 'eu.thethings.network'                                       # Host for TheThingsNetwork
ttn_port = 1883                                                         # TTN service Port
ttn_topic = '+/devices/+/up'                                            # TTN topic
ttn_user = 'iotappan'                                                   # TTN Application's name
ttn_key = 'ttn-account-v2.myG4JDRyLI_p3ylliDwH72pX7bkdRBRL8-fmWpJ0jio'  # TTN Application's Access Key
ttn_dev_e = 'iotappan-dev-e'                                            # device E name
ttn_dev_f = 'iotappan-dev-f'                                            # device F name

'''
END THE THINGS NETWORK
#######################################
'''

'''
#######################################
BEGIN DEVICE CLASS
'''
class Device :

    def __init__(self, name, device_id) :
        self.name = name
        self.device_id = device_id
        self.assigned_profile = None

    def getName() :
        return self.name

    def getID() :
        return self.device_id

    def getProfile() :
        return self.assigned_profile

    def setProfile(given_profile) :
        self.assigned_profile = given_profile

    def __str__(self) :
        return ("Device Name : " + self.name + ", Device ID : " + self.device_id)

'''
END DEVICE CLASS
#######################################
'''

'''
#######################################
BEGIN CLIENT SETTINGS
Settings for the client: callbacks, functions and variables for the gateway client
'''

# Variables for devices    print ("Device Name")
payload_E = ""
payload_F = ""
filename = 'devices.txt'
devices = [None] * 0

# Function for uploading devices : creates an empty list and then appends the devices from the file
def upload_devices() :
    devices = [None] * 0
    with open(filename) as devfile :
        lines = [line.rstrip() for line in devfile]
        for element in lines :
            attributes = element.split(" ")
            devices.append(Device(attributes[0], attributes[1]))
    return devices

# Function for getting a device from a list of devices given the device_id
def get_device(device_id, devices) :
    for element in devices :
        if (element.getID() == device_id) :
            return element
        else :
            print ("No device with ID " + device_id + " found.")

# Function for assigning a given profile to a device given the device id and a device list
def assign_profile(device_id, profile, devices) :
    for element in devices :
        if (element.getID() == device_id) :
            element.setProfile(profile)
            print ("Profile assigned")
        else :
            print ("No device with ID " + device_id + " found.")


# Callback for connection
def on_connect(client, userdata, flags, rc) :           # connect callback for datarec in TTN
    print ("Connected with result code " + str(rc))

# Callback for subscription
def on_subscribe(client, userdata, mid, granted_qos) :
    print ("Subscribed")

# Callback for message event
def on_message(client, userdata, message) :
    print("\n***********************************")

    global devices
    received_message = json.loads(message.payload)
    sender_device = get_device(received_message['dev_id'], devices)
    assign_profile(sender_device.getID(), received_message['profile_id'], devices)

    print ("A message has been received")
    print ("Sender Device : " + received_message['dev_id'])
    print ("Device Name : " + sender_device.getName() )
    print ("Profile Required : " + received_message['profile_id'])

    print("***********************************\n")

# Setting up Data Receiver from TTN
client = paho.Client("Gateway")                        # create client for data receiver from TTN
client.on_message = on_message                         # define what to do when a message is received
client.on_subscribe = on_subscribe                     # event handler
client.username_pw_set(ttn_user, password=ttn_key)     # access with the right credentials
client.connect(ttn_host, ttn_port, keepalive=60)       # establish connection
client.subscribe(ttn_topic, qos=1)

'''
END CLIENT SETTINGS
#######################################
'''

'''
#######################################
BEGIN MAIN
'''

devices = upload_devices()
for element in devices :
    print (element)

client.loop_start()
client.loop_forever()

'''
END MAIN
#######################################
'''
