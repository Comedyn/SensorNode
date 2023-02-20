# import necessary libraries
import io
import sys
import fcntl
import time
import copy
import string
import logging
from AtlasI2C import (
     AtlasI2C
)

log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
logging.basicConfig(filename="main.log", level=logging.INFO, format=log_format)

# define functions
def get_atlasdevices():
    # assign variables
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1]
            response = device.query("name,?").split(",")[1]

        except IndexError:
            continue

        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))

    if len(device_list) == 0:
        logging.warning("(EZO) EZO sensor is not connected.")
        exit(1)

    else:
        logging.info("(EZO) {len(device_list)} EZO sensor is connected.")
        return device_list


def read():
    # assign variables
    data = {}
    device_list = get_atlasdevices()
    DOsensor = ['EC','Sal','TDS','GS']

    try:
        # read data from EZO sensors
        logging.info("(EZO) Reading EZO data...")
        for dev in device_list:
            dev.write("R")

        time.sleep(1)
        
        # print data from EZO sensors
        for dev in device_list:
            dictkey = dev.read().split(' ')
            dictvalue = dictkey[4].split(',')
            
            # check for multiple outputs (EC)
            if len(dictvalue) > 1:
                for x in range(0,4):
                    data[DOsensor[x]]= dictvalue[x].rstrip('\x00')
                    
            # else its single output (PH | ORP | RTD)
            else:
                data[dictkey[1]] = dictvalue[0].rstrip('\x00')
        
        if len(data) != 0:
            logging.info("(EZO) EZO Successful.")
            print("(EZO) EZO Successful.")
            return data
        else:
            logging.warning("(EZO) EZO Unsuccessful.")
            exit(1)
            
    except Exception as err:
        logging.warning("(EZO) Ezo has encountered an error:\n%s", err)
        exit(1)

def main():
    # assign variables
    device_list = get_atlasdevices()
    data = {}
    DOsensor = ['EC','Sal','TDS','GS']
    
    try:
        # read data from EZO sensors
        for dev in device_list:
            dev.write("R")
        
        time.sleep(1)
        
        # print data from EZO sensors
        for dev in device_list:
            dictkey = dev.read().split(' ')
            dictvalue = dictkey[4].split(',')
            
            # check for multiple outputs (EC)
            if len(dictvalue) > 1:
                for x in range(0,4):
                    print(DOsensor[x]+' :\t'+dictvalue[x])
                    data[DOsensor[x]]= dictvalue[x].rstrip('\x00')
                    
            # else its single output (PH | ORP | RTD)
            else:
                print(dictkey[1]+' :\t'+dictvalue[0])
                data[dictkey[1]] = dictvalue[0].rstrip('\x00')
                
        logging.info(data)
        return data
            
    except Exception as err:
        logging.critical("(EZO) Ezo has encountered an error:\n%s", err)
        exit(1)

if __name__ == '__main__':
    main()



# ~ def get_data(data):
    # ~ #get values from key, else return 0
    # ~ ph = data.get('pH',0.0)
    # ~ orp = data.get('ORP',0.0)
    # ~ ec = data.get('EC',0.0)
    # ~ sal = data.get('Sal',0.0)
    # ~ turb = data.get('TDS',0.0)
    # ~ gs = data.get('GS',0.0)
    # ~ rtd = data.get('RTD',0.0)
    # ~ return ph, orp, ec, sal, turb, gs, rtd, do, leak
