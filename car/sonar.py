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


def get_echo_micros():

    set_output_pin_value(SONAR_TRIGGER_PIN, True)
    delay_micros(10)
    set_output_pin_value(SONAR_TRIGGER_PIN, False)

    while query_input_pin(SONAR_ECHO_PIN) == False:
        pass

    start = query_micros()

    while query_input_pin(SONAR_ECHO_PIN) == True:
        pass

    end = query_micros()

    return end - start


def compute_distance_meters(echo_micros):

    distance_meters = echo_micros * 0.0003432
    return distance_meters


def compute_distance_feet(echo_micros):

    distance_feet = compute_distance_meters(echo_micros) * 3.28084
    return distance_feet


if __name__ == '__main__':
    for i in range(100):
        import time
        echo_micros = get_echo_micros()
        print("meters = {}".format(compute_distance_meters(echo_micros)))
        print("feet   = {}\n".format(compute_distance_feet(echo_micros)))
        time.sleep(0.1)

