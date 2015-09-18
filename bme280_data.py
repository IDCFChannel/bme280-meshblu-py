#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import json
import bme280
import requests
from config import conf

def sensing():
    return bme280.readData()

def main():
    # HTTP
    url = "http://{0}/data/{1}".format(conf["IDCF_CHANNEL_URL"],
                                       conf["TRIGGER_1_UUID"])
    headers = {
        "meshblu_auth_uuid": conf["TRIGGER_1_UUID"],
        "meshblu_auth_token": conf["TRIGGER_1_TOKEN"]
    }

    payload = {"trigger":"on"}

    while True:
        retval = sensing()
        if retval:
             print("temperature: {}".format(retval["temperature"]))
             if float(retval["temperature"]) > conf["THRESHOLD"]:
                 print("threshold over: {0} > {1}".format(float(retval["temperature"]),
                                     conf["THRESHOLD"]))
                 r = requests.post(url, headers=headers, data=payload)
        sleep(5)

if __name__ == '__main__':
    main()
