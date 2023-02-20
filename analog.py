# imports
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import logging

log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
logging.basicConfig(filename="main.log", level=logging.INFO, format=log_format)

def read():
    # assign variables
    i2c = busio.I2C(board.SCL, board.SDA)

    # check if ads is connected
    try:
        # assign ads
        ads = ADS.ADS1115(i2c)
        
        # assign channels
        chan0 = AnalogIn(ads, ADS.P0)
        chan1 = AnalogIn(ads, ADS.P1)
        chan2 = AnalogIn(ads, ADS.P2)
        chan3 = AnalogIn(ads, ADS.P3)

        # set channels settings
        ads.gain = 1 # 2/3 | 1 | 2 | 4 | 8 | 16
        ads.mode = 0 #continuous = 0 | single = 256
        
        # assign variables
        data = {'do': 0.0, 'leak': 0.0, 'battery': 0.0}
        
        # assign channels value
        # value0 = chan0.value
        # value1 = chan1.value
        # value2 = chan2.value
        # value3 = chan3.value
        
        # assign channel voltage (V)
        do = chan0.voltage
        leak = chan1.voltage
        battery = chan2.voltage
        test = chan3.voltage
        
        logging.info("(ANALOG) Analog is connected...")
        
        # assign keys to values
        logging.info("(ANALOG) Reading analog data...")
        data['do'] = do
        data['leak'] = leak
        data['battery'] = battery
        data['test'] = test
                
        # return data as dictionary
        logging.info("(ANALOG) Analog Successful.")
        print("(ANALOG) Analog Successful.")
        return data

        # unused variables
        # value0, value1, value2, voltage2, value3, voltage3
        
    except ValueError:
        logging.warning('(ANALOG) Analog is not connected.')
        exit(1)

    except Exception as err:
        logging.warning("(ANALOG) Analog has encountered an error:\n%s", err)
        exit(1)


if __name__ == '__main__':
    while True:
        print(read())
        time.sleep(1)

# ~ percent = (chan0.voltage/0.450)*100
# ~ probeval = (chan0.voltage/11)*1000
# ~ if chan3.voltage > 0.500:
        # ~ print(">>LEAK DETECTED<<")
