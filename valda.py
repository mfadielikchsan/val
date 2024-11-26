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
url = ""

# Function to send data to the database
def send_data(sensor_name, status):
    payload = {"sensor": sensor_name, "status": status}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Data sent successfully: {payload}")
        else:
            print(f"Failed to send data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data: {e}")

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
        if mt_state == GPIO.LOW:  # Motor running
            if last_sent_sensor != "MT":
                send_data("MT", 1)
                last_sent_sensor = "MT"
        else:
            # Check other sensors if MT is not running
            if td_state == GPIO.LOW and last_sent_sensor != "TD":
                send_data("TD", 1)
                last_sent_sensor = "TD"
            elif es_state == GPIO.LOW and last_sent_sensor != "ES":
                send_data("ES", 1)
                last_sent_sensor = "ES"
            elif c1_state == GPIO.LOW and last_sent_sensor != "C1":
                send_data("C1", 1)
                last_sent_sensor = "C1"
            elif c2_state == GPIO.LOW and last_sent_sensor != "C2":
                send_data("C2", 1)
                last_sent_sensor = "C2"
            else:
                # If no sensors are active, send error status
                if last_sent_sensor != "ERROR":
                    send_data("ERROR", 0)
                    last_sent_sensor = "ERROR"

        time.sleep(0.5)  # Debouncing delay
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
