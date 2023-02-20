# Import necessary libraries
import pandas as pd # pip install pandas
from time import sleep
from multiprocessing import Queue
import logging

# Logging formatting
log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
# Configure logging file
logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.INFO, format=log_format)

# Note: Pressure depth by meter can be directly calculated in the depth.py script instead of manual calculations. Sorry.
# Define pressure_depth with input argument pressure_mbar
def pressure_depth(pressure_mbar):
    # Convert pressure from mbar to bar
    pressure_bar = pressure_mbar/1000
    # Convert pressure bar to depth in meters
    depth_meter = pressure_bar * 10.197
    # Offset depth in meters
    depth_meter_offset = depth_meter - 10.3
    # Return depth in meters variable
    return depth_meter_offset

# Define dissolved_oxygen with input argument water_oxygen
def dissolved_oxygen(water_oxygen):
    # Set variable for dissolved oxygen in air (Recorded data before placing in water in Voltage)
    atmospheric_oxygen = 0.6
    # Calculate the dissolved oxygen in percent_saturation
    percent_oxygen = (water_oxygen/atmospheric_oxygen) * 100
    # Return dissolved oxygen variable
    return percent_oxygen

# Define main function
def main(queue):
    # Set data_collected variable to 0
    data_collected = 0
    logging.info("(PROCESS) Grabbing message queue for processing.")
    # Wait for queue for up to 100 seconds
    for i in range(200):
        # If queue is empty, check again in 0.5 seconds
        if queue.empty():
            sleep(0.5)
            continue
        # If queue is not empty, grab message queue and store as dictionary data
        else:
            # Log info for queue found
            logging.info("(PROCESS) Data in message queue was found.")
            # Grab message queue as dictionary data
            data = queue.get()
            # Exit 'for' loop
            break
    
    # Log info on processing data
    logging.info("(PROCESS) Processing data...")
    print("Processing...")
    # Check if dictionary data is empty
    if len(data) != 0:
        # Create new dictionary new_data
        new_data = {}
        try:
            # grab value (value is a dictionary) from key inside dictionary data
            for _, row in data.items():
                # grab key and value from dictionary value
                for key, value in row.items():
                    # convert all value to float
                    float_value = float(value)
                    # if key is lat or lon, convert to float in 5 decimal places
                    if key == 'lat' or key == 'lon':
                        rounded_value = round(float_value, 5)
                    # if key is depth, start pressure_depth function and convert to 2 decimal places
                    elif key == 'depth':
                        rounded_value = round(pressure_depth(value), 2)
                    # if key do, start dissolved_oxygen function and convert to 2 decimal places
                    elif key == 'do':
                        rounded_value = round(dissolved_oxygen(value), 2)
                    # other keys, convert to 2 decimal places
                    else:
                        rounded_value = round(float_value, 2)
                        # if key is leak and below 250 value, convert to boolean False
                        if key == 'leak' and value < 250.0:
                            rounded_value = False
                        # else key is leak and above or equal to 250, convert to boolean true
                        elif key == 'leak' and value >= 250.0:
                            rounded_value = True
                    # log info
                    logging.info(f"(PROCESS) {key} has been processed.")
                    # assign key and value to dictionary new_data
                    new_data[key] = rounded_value
                    
        except Exception as err:
            logging.warning("[FAILED] Processing data has encountered a problem:\n%s", err)
            exit(1)
        # log info
        logging.info("(PROCESS) Importing message queue to dataframe.")
        # convert dictionary to new dataframe df
        df = pd.DataFrame([new_data])
        # add on timestamp to new dataframe df with datetime format
        df['datetime'] = pd.Timestamp('now').strftime('%Y-%m-%d %H:%M:%S')
        # change all columns name to small letters
        df.columns = df.columns.str.lower()
        # if data is collected, set data_collected variable to 1
        data_collected = 1

    else:
        # log warning for no message queue found
        logging.warning("(PROCESS) No data in message queue was found.")
        sleep(0.5)
    
    # check if data_collect variable is 0
    if data_collected == 0:
        # log warning
        logging.warning("(PROCESS) Importing timestamp to dataframe.")
        # if no data collected, set all columns in dataframe df to Null value
        df = pd.DataFrame({'datetime': [None]})
        # add datetime to dataframe df
        df['datetime'] = pd.Timestamp('now').strftime('%Y-%m-%d %H:%M:%S')
    
    # log info about dataframe df
    logging.info("(PROCESS) Data processed:\n%s", df)
    logging.info("(PROCESS) Sending message queue.")
    logging.info("[SUCCESS] Processing was successful.")
    print("Processed.")
    # return variable dataframe df
    return df    

# Runs the program if running directly from this script
if __name__ == '__main__':
    # create new dictionary testdata
    testdata = {}
    # testdata = {'depth': {'Depth':'123'}, 'analog': {'Leak':'-1', 'do': 123}, 'ezo': {'Ph':3.012}}
    # create new message queue
    queue = Queue()
    queue.put(testdata)
    print(main(queue))

