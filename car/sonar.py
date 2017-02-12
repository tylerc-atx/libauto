from car import STORE
from car.gpio import (setup_output_on_pin,
                      setup_input_on_pin,
                      set_output_pin_value,
                      query_input_pin,
                      delay_micros,
                      query_micros)


SONAR_TRIGGER_PIN = STORE.get('SONAR_TRIGGER_PIN', 27)
SONAR_ECHO_PIN    = STORE.get('SONAR_ECHO_PIN',    17)
SONAR_MAX_DISTANCE_METERS_CUTOFF = STORE.get('SONAR_MAX_DISTANCE_METERS_CUTOFF', 1.0)


setup_output_on_pin(SONAR_TRIGGER_PIN)
setup_input_on_pin(SONAR_ECHO_PIN)

set_output_pin_value(SONAR_TRIGGER_PIN, False)
delay_micros(200000)  # 0.2 seconds


def _wait_for(pin, value, timeout):
    """
    Wait for the given pin to become the given value, or time out.
    The `timeout` parameter is in seconds.
    Returns True if the pin became the value before the timeout, or
    returns False if the timeout was reached.
    """
    timeout_micros = timeout * 1000000
    start = query_micros()
    while True:
        for _ in range(10000):
            if query_input_pin(pin) == value:
                return True
        end = query_micros()
        if (end - start) > timeout_micros:
            return False


def emit():
    """
    Triggers the sonar sensor to emit a small sound.
    """

    set_output_pin_value(SONAR_TRIGGER_PIN, True)
    delay_micros(10)
    set_output_pin_value(SONAR_TRIGGER_PIN, False)

    return _wait_for(SONAR_ECHO_PIN, True, 2.0)


def detect_echo():
    """
    Waits for the sonar sensor to report the time elapsed
    between when it emitted the sound and when it detected
    the returning sound.
    """

    return _wait_for(SONAR_ECHO_PIN, False, 2.0)


def echo_time():
    """
    Computes the amount of time (in seconds) between
    a call to `emit()` and a call to `detect_echo()`.
    """

    e = emit()
    start = query_micros()
    if not e:
        return float('inf')

    d = detect_echo()
    end = query_micros()
    if not d:
        return float('inf')

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
    if distance_meters >= SONAR_MAX_DISTANCE_METERS_CUTOFF:
        distance_meters = float('inf')
    return distance_meters


def _set_sonar_pins():
    """
    Ask the user to input the sonar sensor parameters, and then
    store them in the database. To use the sonar sensor, the
    process should be restarted after a call to this function.
    """

    trigger_pin_index = int(input("enter the trigger pin index: "))
    echo_pin_index = int(input("enter the echo pin index: "))
    max_cutoff = float(input("enter the max sonar cutoff distance: "))

    STORE.put('SONAR_TRIGGER_PIN',  trigger_pin_index)
    STORE.put('SONAR_ECHO_PIN',  echo_pin_index)
    STORE.put('SONAR_MAX_DISTANCE_METERS_CUTOFF', max_cutoff)

    print("process restart required")

