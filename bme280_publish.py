#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from time import sleep
import json
import sys
import bme280
import requests
from config import conf

def sensing():
    return bme280.readData()

def on_connect(client, userdata, rc):
    print("Connected with result code {}".format(rc))

def on_publish(client, userdata, mid):
    print("publish: {}".format(mid))

def main():
    # MQTT
    client = mqtt.Client(client_id='',
	                 clean_session=True, protocol=mqtt.MQTTv311)
    client.username_pw_set(conf["TRIGGER_1_UUID"], conf["TRIGGER_1_TOKEN"])
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(conf["IDCF_CHANNEL_URL"], 1883, 60)

    # HTTP
    url = "http://{0}/data/{1}".format(conf["IDCF_CHANNEL_URL"],
                                       conf["TRIGGER_1_UUID"]) 
    headers = {
        "meshblu_auth_uuid": conf["TRIGGER_1_UUID"],
        "meshblu_auth_token": conf["TRIGGER_1_TOKEN"]
    };
    payload = {"trigger":"on"}

    while True:
        retval = sensing()
        if retval:
             message = json.dumps({"devices":
	                      [conf["ACTION_1_UUID"],
	                       conf["ACTION_2_UUID"]],
                              "payload": retval})
             print(message)
             client.publish("message",message)
               
             if retval["temperature"] > conf["THRESHOLD"]:
                 r = requests.post(url, headers=headers, data=payload)
        sleep(5)

if __name__ == '__main__':
    main()
