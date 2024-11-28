else:
                # Check if all sensors are inactive
                if td_state == GPIO.HIGH and es_state == GPIO.HIGH and c1_state == GPIO.HIGH and c2_state == GPIO.HIGH and mt_state == GPIO.HIGH:
                    if last_sent_sensor != "ERROR":
                        send_data("ERROR", 0)
                        last_sent_sensor = "ERROR"
                # If any sensor is active, do nothing, don't send error
                elif td_state == GPIO.LOW or es_state == GPIO.LOW or c1_state == GPIO.LOW or c2_state == GPIO.LOW or mt_state == GPIO.LOW:
                    pass  # Do nothing as the sensor state will already be handled
