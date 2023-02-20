# import necessary libraries
import serial
from serial import SerialException
from time import sleep
import logging

log_format = "%(asctime)s-%(levelname)s-%(name)s-%(message)s"
logging.basicConfig(filename="main.log", level=logging.INFO, format=log_format)

def convert_nmea_to_readable(gps_data):
    latitude_decimal = 0
    longitude_decimal = 0
    gps_nmea = gps_data[1].split(',')
    latitude, dlatitude, longitude, dlongitude  = gps_nmea[0:4]
    
    lat_parts = latitude.split('.')
    lon_parts = longitude.split('.')
    
    lat_degrees = float(lat_parts[0][:2])
    lat_minutes = float(lat_parts[0][2:] + '.' + lat_parts[1])
    lon_degrees = float(lon_parts[0][:3])
    lon_minutes = float(lon_parts[0][3:] + '.' + lon_parts[1])
    
    latitude_decimal = lat_degrees + (lat_minutes/60)
    longitude_decimal = lon_degrees + (lon_minutes/60)
    
    if dlatitude == 'S':
        latitude_decimal = -latitude_decimal
    if dlongitude == 'W':
        longitude_decimal = -longitude_decimal
    
    return latitude_decimal, longitude_decimal

def read():
    latitude = None
    longitude = None
    time = 40
    
    # Check for serial connection
    try:
        ser = serial.Serial('/dev/ttyUSB2',115200)
    except SerialException:
        message = "(GPS) GPS is not connected."
        logging.warning(message)
        print(message)
        exit(1)
    
    # Loop for set time seconds
    print(f"(GPS) Reading GPS data... [<{time} Seconds]")
    for i in range(time,0,-1):
        if i % 10 == 0:
            print(f"(GPS) Time left: {i}...")
        
        lines = []
        ser.write(b'AT+CGPS=1\r\n')
        ser.write(b'AT+CGPSINFO\r\n')
        for i in range(0,4):
            serial_line = str(ser.readline())
            lines.append(serial_line.strip())
        # print(lines)
        for item in lines:
            if item.find(':') != -1:
                index = lines.index(item)
                data = lines[index]
                # print(data)
        gps_data = str(data).split(': ')
        if ',,,,,,,,' in gps_data[1]:
            sleep(1)
            continue
        else:
            print("(GPS) GPS Successful.")
            latitude, longitude = convert_nmea_to_readable(gps_data)
            gps_decimal = {'lat':latitude, 'lon':longitude}
            # print('Lat: '+ str(latitude), '\nLong: '+ str(longitude))
            break
        
        ser.flushInput()

    if latitude == None and longitude == None:
        gps_decimal = {}
        print("(GPS) GPS Unsuccessful.")
    ser.close()
    return gps_decimal


if __name__ == "__main__":
    print(read())
