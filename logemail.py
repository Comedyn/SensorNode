# -*- coding: utf-8 -*-
"""
READ LOGGING FILE AND SEND EMAIL
"""

import logging
import yagmail
import time

try:
    print("Connecting to server...")
    yag = yagmail.SMTP("beggear@gmail.com", "ykmvzxjwwhediuef")
    print("Connected.")
except Exception as err:
    print(err)

subject = "Client1 - CRITICAL"
content = "There is an error in the software."

logging.basicConfig(filename='main.log',level=logging.DEBUG)

while True:
    # Open logfile and read the last line
    with open("main.log","r") as f:
        log = f.readlines()[-10]
    
    # Check for critical in line
    if "CRITICAL" in log:
        try:
            print("Sending email to recipient...")
            yag.send("lowziyi08@gmail.com", subject, content)
            print("Email sent successfully.")
            break
        except Exception as err:
            print(err)
