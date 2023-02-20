# imports
from time import sleep
import RPi.GPIO as GPIO

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sensorrelay = 24
commsrelay = 23
GPIO.setup(sensorrelay, GPIO.OUT)
GPIO.setup(commsrelay, GPIO.OUT)
	
def main():
	print(relaysoff())

def sensorson():
	GPIO.output(sensorrelay, GPIO.HIGH)
	string = "(RELAY) Sensors turned ON."
	return string

def sensorsoff():
	GPIO.output(sensorrelay, GPIO.LOW)
	string = "(RELAY) Sensors turned OFF."
	return string
	
def commson():
	GPIO.output(commsrelay, GPIO.HIGH)
	string = "(RELAY) 4G turned ON."
	return string
	
def commsoff():
	GPIO.output(commsrelay, GPIO.LOW)
	string = "(RELAY) 4G turned OFF."
	return string

def relayson():
	sensorson()
	commson()
	string = "(RELAY) Both relays turned ON."
	return string

def relaysoff():
	sensorsoff() 
	commsoff() 
	string = "(RELAY) Both relays turned OFF."
	return string

if __name__ == "__main__":
	try:
		main()
	except Exception as err:
		print("Relay Script has encountered an error: ", err)
