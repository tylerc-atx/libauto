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
    """
    Triggers the sonar sensor to emit a small sound.
    """

    set_output_pin_value(SONAR_TRIGGER_PIN, True)
    delay_micros(10)
    set_output_pin_value(SONAR_TRIGGER_PIN, False)

    while query_input_pin(SONAR_ECHO_PIN) == False:
        pass


def detect_echo():
    """
    Waits for the sonar sensor to report the time elapsed
    between when it emitted the sound and when it detected
    the returning sound.
    """

    while query_input_pin(SONAR_ECHO_PIN) == True:
        pass


def echo_time():
    """
    Computes the amount of time (in seconds) between
    a call to `emit()` and a call to `detect_echo()`.
    """

    emit()
    start = query_micros()

    detect_echo()
    end = query_micros()

    return (end - start) / 1000000.0


def query_distance(sound_speed=343.2):
    """
    Uses the `echo_time()` function and the provided
    sound speed (via the `sound_speed` parameter) to
    compute the distance between the car and the first
    obstacle which reflects sound well.

    The default for `sound_speed` (343.2) is in meters
    per second.
    """

    distance_meters = (echo_time() / 2.0) * sound_speed
    return distance_meters


if __name__ == '__main__':
    import time
    for i in range(100):
        print("meters = {}".format(query_distance()))
        time.sleep(0.1)

