import requests
import time
import RPi.GPIO as GPIO

# Konfigurasi GPIO
TD = 17  # Push button start
ES = 27  # Emergency stop
C1 = 22  # Camera 1
C2 = 5   # Camera 2
MT = 6   # Motor running sensor

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins as input with pull-up resistors
GPIO.setup(TD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ES, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# URL target
url = "http://10.246.142.20/pdgeneral/kirim_data/sensor2/"

# Function to send data to the database
def send_data(param):
    full_url = f"{url}{param}"
    response = requests.get(full_url)

# Variable to track the last sent status
last_sent_sensor = None

try:
    while True:
        # Read the state of sensors
        td_state = GPIO.input(TD)
        es_state = GPIO.input(ES)
        c1_state = GPIO.input(C1)
        c2_state = GPIO.input(C2)
        mt_state = GPIO.input(MT)

        # Priority: Check MT sensor first
        if mt_state == GPIO.HIGH:  # Motor running
            if last_sent_sensor != "MT":
                send_data("MT")
                print("MT")
                last_sent_sensor = "MT"
        else:
            # Check other sensors if MT is not running
            if td_state == GPIO.HIGH and es_state == GPIO.HIGH and c1_state == GPIO.HIGH and c2_state == GPIO.HIGH and last_sent_sensor != "10":
                if last_sent_sensor == "MT":
                    send_data("10") #NF
                    print("10")
                    last_sent_sensor = "10"
            elif td_state == GPIO.LOW and last_sent_sensor != "11":
                send_data("11") #TD
                last_sent_sensor = "11"
                print("11")
            elif es_state == GPIO.LOW and last_sent_sensor != "12":
                send_data("12") #ES
                print("12")
                last_sent_sensor = "12"
            elif c1_state == GPIO.LOW and last_sent_sensor != "13":
                send_data("13") #C1
                print("13")
                last_sent_sensor = "13"
            elif c2_state == GPIO.LOW and last_sent_sensor != "14":
                send_data("14")
                print("14")
                last_sent_sensor = "14"


        time.sleep(0.5)  # Debouncing delay
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()

