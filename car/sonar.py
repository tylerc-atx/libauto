from car import STORE
from car.gpio import (setup_output_on_pin,
                      setup_input_on_pin,
                      set_output_pin_value,
                      query_input_pin,
                      delay_micros,
                      query_micros)


SONAR_TRIGGER_PIN = STORE.get('SONAR_TRIGGER_PIN', 27)
SONAR_ECHO_PIN    = STORE.get('SONAR_ECHO_PIN',    17)


setup_output_on_pin(SONAR_TRIGGER_PIN)
setup_input_on_pin(SONAR_ECHO_PIN)

set_output_pin_value(SONAR_TRIGGER_PIN, False)
delay_micros(100000)  # 0.1 seconds


def emit():

    set_output_pin_value(SONAR_TRIGGER_PIN, True)
    delay_micros(10)
    set_output_pin_value(SONAR_TRIGGER_PIN, False)

    while query_input_pin(SONAR_ECHO_PIN) == False:
        pass


def detect_echo():

    while query_input_pin(SONAR_ECHO_PIN) == True:
        pass


def echo_time():

    emit()
    start = query_micros()

    detect_echo()
    end = query_micros()

    return end - start


def echo_distance():

    distance_meters = echo_time() * 0.0003432
    return distance_meters


if __name__ == '__main__':
    import time
    for i in range(100):
        print("meters = {}".format(echo_distance()))
        time.sleep(0.1)

