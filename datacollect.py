# Import necessary libraries
from ezo import read as readEzo
from analog import read as readAnalog
from depth import read as readDepth
from gps import read as readGPS
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import logging

# Logging formatting
log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
# Configure logging file
logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.INFO, format=log_format)

# Define ezo_sensor with argument queue
def ezo_sensor(queue):
    # place returned value from readezo into variable data
    data = readEzo()
    # place dictionary with key and value into queue
    queue.put(("ezo", data))

# Define analog_sensor with argument queue
def analog_sensor(queue):
    # place returned value from readanalog into variable data
    data = readAnalog()
    # place dictionary with key and value into queue
    queue.put(("analog", data))

# Define depth_sensor with argument queue
def depth_sensor(queue):
    # place returned value from readdepth into variable data
    data = readDepth()
    # place dictionary with key and value into queue
    queue.put(("depth", data))

# Define gps_sensor with argument queue
def gps_data(queue):
    # place returned value from readgps into variable data
    data = readGPS()
    # place dictionary with key and value into queue
    queue.put(("gps", data))

def main():
    logging.info("(COLLECT) Collecting data...")
    # create new queue
    queue = Queue()
    sensordata = {}
    try:
        # start multi-threading using ThreadPoolExecutor with arguments script and queue
        with ThreadPoolExecutor() as executor:
            executor.submit(ezo_sensor, queue)
            executor.submit(analog_sensor, queue)
            executor.submit(depth_sensor, queue)
            executor.submit(gps_data, queue)
            # end multi-threading
            executor.shutdown()
            # check if queue is empty, else grab queue
            while not queue.empty():
                # grab queue and assign them into key and variable
                key, value = queue.get()
                # assign key and value to dictionary sensordata
                sensordata[key] = value
        logging.info("(COLLECT) Data collected:\n%s", sensordata)
        logging.info("(COLLECT) Sending message queue.")
        logging.info("[SUCCESS] Collection was successful.")
        # return variable sensordata
        return sensordata
        
    except Exception as err:
        logging.exception("[FAILED] Collecting data has encountered an issue:\n%s", err)
        exit(1)
    
# Runs the program if running directly from this script
if __name__ == "__main__":
    print(main())
