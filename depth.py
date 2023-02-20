# imports
import ms5837
import time
import logging

log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
logging.basicConfig(filename="main.log", level=logging.INFO, format=log_format)
# assign sensor
sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

def main():
        try:
                # initialize sensor
                if not sensor.init():
                        logging.warning("(DEPTH) Sensor could not be initialized")
                        exit(1)

                while True:
                        # read sensor
                        if sensor.read():
                                print(("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
                                sensor.pressure(), # Default is mbar (no arguments)
                                sensor.pressure(ms5837.UNITS_psi), # Request psi
                                sensor.temperature(), # Default is degrees C (no arguments)
                                sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
                        else:
                                message = "(DEPTH) Sensor read failed!"
                                logging.critical(message)
                                print(message)
                                exit(1)
        except IOError:
                message = "(DEPTH) Depth sensor is not connected."
                logging.warning(message)
                print(message)
                exit(1)
        except Exception as message:
                logging.critical(message)
                print('Error:', message)
                exit(1)
                        
def read():
        try:
                # initialize sensor
                if not sensor.init():
                        logging.critical("(DEPTH) Depth could not be initialized." )
                        time.sleep(1)
                else:
                    logging.info("(DEPTH) Depth sensor is connected.")
                        
                if sensor.read():
                        logging.info("(DEPTH) Reading depth data...")
                        data = {'depth': 0.0}
                        data['depth'] = sensor.pressure()
                        logging.info("(DEPTH) Depth Successful.")
                        print("(DEPTH) Depth Successful.")
                        
                        return data
                        
                        # unused variables:
                        # sensor.pressure(ms5837.UNITS_psi), sensor.temperature(), sensor.temperature(ms5837.UNITS_Farenheit)
                
                else:
                        logging.critical("(DEPTH) Depth Unsuccessful.")
                        exit(1)
                        
        except IOError:
                logging.warning("(DEPTH) Depth sensor is not connected.")
                exit(1)
                
        except Exception as err:
                logging.warning('(DEPTH) Depth has encountered an error:\n%s', err)
                exit(1)
                
if __name__ == "__main__":
    main()
