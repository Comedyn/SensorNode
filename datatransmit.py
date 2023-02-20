from sqlalchemy import create_engine, MetaData, Table, Column, Float, DateTime, Boolean
from sqlalchemy.exc import IntegrityError
import logging

log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.DEBUG, format=log_format)

def main():
    print("Transmitting...")
    user = "root"
    password ="mspiout"
    host = "localhost"
    remote_host = "10.13.129.1"
    database = "clients"
    table_name = "client1_data"
    
    port = 3306
    
    # Connect to the local MariaDB database
    try:
        logging.info("(TRANSMIT) Connecting to local MariaDB database.")
        local_db = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
        logging.info("(TRANSMIT) Connected to local MariaDB database.")
    except Exception as err:
        logging.critical("(TRANSMIT) Unable to connect to local MariaDB database: %s", err)
        exit(1)
        
    local_data = local_db.execute(f"SELECT * FROM {table_name} ORDER BY datetime DESC LIMIT 1") # Table should have already been created in datastorage.py
    
    # Connect to the remote MariaDB database (NAS server)
    try:
        logging.info("(TRANSMIT) Connecting to remote MariaDB database.")
        remote_db = create_engine(f"mysql+pymysql://{user}:{password}@{remote_host}:{port}/{database}")
        logging.info("(TRANSMIT) Connected to remote MariaDB database.")
    except Exception as err:
        logging.critical("(TRANSMIT) Unable to connect to remote MariaDB database: %s", err)
        exit(1)
        
    metadata = MetaData()
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
    
    # Check if table_name has been created in remote MariaDB database
    try:
        logging.info(f"(TRANSMIT) Creating table {table_name}.")
        metadata.create_all(remote_db)
    except IntegrityError:
        logging.info(f"(TRANSMIT) Table {table_name} already exists.")
        pass
    
    # Insert the data into the remote MariaDB database (NAS server)
    logging.info("(TRANSMIT) Importing from local to remote MariaDB database.")
    for row in local_data:
        try:
            # Convert datetime.datetime to a string
            datetime_string = row['datetime'].strftime('%Y-%m-%d %H:%M:%S')

            # Insert the data into the remote MariaDB database
            remote_db.execute(f"INSERT INTO {table_name} (datetime, depth, ph, orp, ec, sal, tds, gs, rtd, do, leak, lat, lon, battery) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (datetime_string, row['depth'], row['ph'], row['orp'], row['ec'], row['sal'], row['tds'], row['gs'], row['rtd'], row['do'], row['leak'], row['lat'], row['lon'], row['battery']))
            
        except IntegrityError as err:
            if 'Duplicate' in str(err):
                logging.warning("(TRANSMIT) Duplicate found in remote MariaDB database.")
                pass
                
            else:
                logging.critical("(TRANSMIT) Exception has occured: %s", err)
                exit(1)
    logging.info("[SUCCESS] Transmition was successful.")
    print("Transmitted.")
            
if __name__ == "__main__":
    main()
