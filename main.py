# Import necessary libraries
import relay
import datacollect as collectPy
import dataprocess as processPy
import datastorage as storagePy
import datatransmit as transmitPy
from multiprocessing import Process, Queue
from time import sleep
from datetime import datetime
import logging

# Logging formatting
log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
# Configure logging file
logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.INFO, format=log_format)

# Define collect functions
def collect(queue):
    try:
        # Put returned variable from 'datacollect' script into Message Queue
        queue.put(collectPy.main())
    except Exception as err:
        # Log error
        logging.critical("(MAIN) Collect Script encountered an error:\n%s", err)
        pass

# Define process functions
def process(queue):
    try:
        # Put returned variable from 'dataprocess' script into Message Queue
        queue.put(processPy.main(queue))
    except Exception as err:
        # Log error
        logging.critical("(MAIN) Process Script encountered an error:\n%s", err)
        pass

# Define storage functions
def storage(queue):
    try:
        # Put returned variable from 'datastorage' script into Message Queue
        storagePy.main(queue)
    except Exception as err:
        # Log error
        logging.critical("(MAIN) Storage Script encountered an error:\n%s", err)
        pass

# Define transmit functions
def transmit():
    try:
        # Put returned variable from 'datatransmit' script into Message Queue
        transmitPy.main()
    except Exception as err:
        # Log error
        logging.critical("(MAIN) Transmit Script encountered an error:\n%s", err)
        pass

# Define multi process functions
def multi_process():
    # Define initializing time (mins)
    init_time = 40
    # Create new message queue
    queue = Queue()
    
    # Create processes for multi-processing
    collect_process = Process(target=collect, args=(queue,))
    process_process = Process(target=process, args=(queue,))
    storage_process = Process(target=storage, args=(queue,))
    transmit_process = Process(target=transmit)
    
    # Log info about initializing time
    logging.info(f"(MAIN) Initializing for {init_time} seconds.")
    print("(MAIN) Initializing...")
    
    # Initialize for 40 seconds using 'for' loop
    for i in range(init_time,0,-1):
        # Countdown and print every 10 seconds
        if i % 10 == 0:
            print(f"(MAIN) Time left: {i}...")
        sleep(1)
    print("(MAIN) Starting Processes.")
    
    # Start multi-processing for collect and process
    collect_process.start()
    process_process.start()
    # End multi-processing for collect and process
    collect_process.join()
    process_process.join()
    # Start multi-processing for storage
    storage_process.start()
    # End multi-processing for storage
    storage_process.join()
    # Start multi-processing for transmit
    transmit_process.start()
    # End multi-processing for storage
    transmit_process.join()
    print("(MAIN) Ending Processes.")
   
# Define main functions
def main():
    # Set interval variable (Sampling time in minutes)
    interval = 10
    # Log info about interval set
    logging.info(f"(MAIN) Interval set to every {interval} mins.")

    # Check system datetime every millisecond
    while True:
        # For every set interval, run multi-process function
        if datetime.now().minute % interval == 0:
            print(datetime.now())
            # Turn on relays
            logging.info(relay.relayson())
            # Start multi-process function
            multi_process()
            # Turn off relays once multi-process functions ends
            logging.info(relay.relaysoff())
            sleep(10)

# Runs the program if running directly from this script
if __name__ == "__main__":
    try:
        # Log info
        logging.info("(MAIN) Starting Main Script.")
        # Start main function
        main()
    # If keyboard interrupt, end script
    except KeyboardInterrupt:
        logging.info("(MAIN) Main Script Interrupted.")
        logging.info("(MAIN) Ending Main Script.")
        exit(0)
    # If error in script, end script
    except Exception as err:
        logging.critical("(MAIN) Main script has encountered an error:/n%s",err)
        logging.info("(MAIN) Ending Main Script.")
        exit(1)

