# Import necessary libraries
from sqlalchemy import create_engine, Table, Column, DateTime, Boolean, MetaData, insert, Float
from sqlalchemy.exc import IntegrityError
from time import sleep
import pandas as pd
from queue import Queue
import logging

# Logging formatting
log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
# Configure logging file
logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.INFO, format=log_format)

# Define main function with argument queue
def main(queue):
    # Assign variable according to user, password, host, database and table of the MariaDB database
    u = "root"
    p = "mspiout"
    h = "localhost"
    d = "clients"
    table_name = "client1_data"
    logging.info("(STORAGE) Grabbing message queue for storing.")
    # Wait for queue for 30 seconds
    for i in range(60):
        if queue.empty():
            sleep(0.5)
            continue
        else:
            # If queue is not empty, grab queue and convert to dataframe
            logging.info("(STORAGE) Data in message queue was found.")
            dataframe = pd.DataFrame(queue.get())
            break
        
    # Check connection to local MariaDB
    logging.info("(STORAGE) Storing data...")
    print("Storing...")
    try:
        logging.info("(STORAGE) Connecting to local database.")
        # create engine to connect to the local MariaDB database using assigned variables
        engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{database}"
            .format(host=h, database=d, user=u, password=p))
        # create connection
        connection = engine.connect()
        # create a metadata object to hold the database schema information
        metadata = MetaData()
        logging.info("(STORAGE) Connected to local database.")
    except Exception as err:
        logging.critical("(STORAGE) Connection to local database failed.")
        logging.critical("[FAILED] Storage has encountered an issue:\n%s", err)
        exit(1)
    
    # define table and columns
    table = Table(table_name, metadata,
        Column('datetime', DateTime, primary_key=True),
        Column('depth', Float, nullable=True),
        Column('ph', Float, nullable=True),
        Column('orp', Float, nullable=True),
        Column('ec', Float, nullable=True),
        Column('sal', Float, nullable=True),
        Column('tds', Float, nullable=True),
        Column('gs', Float, nullable=True),
        Column('rtd', Float, nullable=True),
        Column('do', Float, nullable=True),
        Column('leak', Boolean, nullable=True),
        Column('lat', Float, nullable=True),
        Column('lon', Float, nullable=True),
        Column('battery', Float, nullable=True)
    )
    
    # Check if table exists
    try:
        logging.info(f"(STORAGE) Creating table {table_name}")
        # create table
        metadata.create_all(engine)
    except IntegrityError:
        logging.info(f"(STORAGE) Table {table_name} already exists.")
        pass

    logging.info("(STORAGE) Checking for missing values in dataframe.")
    # check for missing column names in dataframe comparing from created table
    for columns in table.c:
        column = str(columns)
        colname = str(column.rsplit('.',1)[-1])
        if colname not in dataframe.columns:
            if colname == 'datetime':
                logging.warning(f"(STORAGE) Missing {colname} in dataframe - replacing with datetime")
                dataframe[colname] = pd.Timestamp('now').strftime('%Y-%m-%d %H:%M:%S')
            else:
                logging.warning(f"(STORAGE) Missing {colname} in dataframe - replacing with null")
                dataframe[colname] = None
    
    # query for inserting created table
    query = insert(table).values(
        datetime=dataframe.at[0,'datetime'],
        depth=dataframe.at[0,'depth'],
        ph=dataframe.at[0,'ph'],
        orp=dataframe.at[0,'orp'],
        ec=dataframe.at[0,'ec'],
        sal=dataframe.at[0,'sal'],
        tds=dataframe.at[0,'tds'],
        gs=dataframe.at[0,'gs'],
        rtd=dataframe.at[0,'rtd'],
        do=dataframe.at[0,'do'],
        leak=dataframe.at[0,'leak'],
        lat=dataframe.at[0,'lat'],
        lon=dataframe.at[0,'lon'],
        battery=dataframe.at[0,'battery']
    )
    
    try:
        logging.info("(STORAGE) Importing dataframe to local MariaDB.")
        # execute query through connection to MariaDb database
        connection.execute(query)
        logging.info("(STORAGE) Stored Data:\n%s", dataframe)
        logging.info("(STORAGE) Dataframe has been imported to local MariaDB.")
        # close connection to MariaDb database
        connection.close()
        logging.info("[SUCCESS] Storage was successful.")
        exit(0)
    except Exception as err:
        logging.critical("(STORAGE) Importing to MariaDB failed.")
        logging.critical("[FAILED] Storage has encountered an issue:\n%s", err)
        connection.close()
        exit(1)
    
if __name__ == '__main__':
    testdata = {'depth':[12],'ph':[6],'datetime':['2022-01-01 11:11:20']} # Change datetime for testing
    queue=Queue()
    queue.put(testdata)
    main(queue)
