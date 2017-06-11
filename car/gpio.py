###############################################################################
#
# Copyright (c) 2017 AutoAuto, LLC
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from AutoAuto, LLC.
#
###############################################################################

"""
This module is an adapter for the GPIO interface of whatever SBC you are using.

If you're using a Raspberry Pi, this module will internally use the WiringPi library,
and all `pin_index` parameters in this module use the Broadcom GPIO pin numbering system
(aka, the _BCM_ pin numbers). See: https://pinout.xyz/
"""

__all__ = ['setup_pwm_on_pin', 'setup_output_on_pin', 'setup_input_on_pin'
           'set_pin_pwm_value', 'set_output_pin_value', 'query_input_pin',
           'read_pin_pwm_value', 'delay_micros', 'query_micros']


import os
os.environ['WIRINGPI_GPIOMEM'] = "1"
import wiringpi as wpi
wpi.wiringPiSetupGpio()


PWM_RANGE = 100


def setup_pwm_on_pin(pin_index):
    """
    Configure the given `pin_index` to use software-driven PWM output. You
    may use the `set_pin_pwm_value()` function on this pin after invoking
    this function.

    See this module's docstring for information about `pin_index`.
    """
    wpi.pinMode(pin_index, 1)  # 0=input, 1=output, 2=hardPWM
    wpi.softPwmCreate(pin_index, 0, PWM_RANGE)


def setup_output_on_pin(pin_index):
    """
    Configure the given `pin_index` to be plain digital output. You may
    use the `set_output_pin_value()` function on this pin after invoking this
    function.

    See this module's docstring for information about `pin_index`.
    """
    wpi.pinMode(pin_index, 1)  # 0=input, 1=output, 2=hardPWM


def setup_input_on_pin(pin_index):
    """
    Configure the given `pin_index` to be plain digital input. You may
    use the `query_input_pin()` function on this pin after invoking this
    function.

    See this module's docstring for information about `pin_index`.
    """
    wpi.pinMode(pin_index, 0)  # 0=input, 1=output, 2=hardPWM


def set_pin_pwm_value(pin_index, value):
    """
    Set the given `pin_index` to have a PWM output of `value`. The `value` parameter
    should be in the range [0, 100], representing the percentage of time the output
    is _high_ (aka, the PWM "duty cycle").

    This pin must have previously been configured using a call to `setup_pwm_on_pin()`.
    """
    value = int(value / 100.0 * PWM_RANGE)
    wpi.softPwmWrite(pin_index, value)


def set_output_pin_value(pin_index, value):
    """
    Set the given `pin_index` to have a digital output of `value`. The `value` parameter
    should be either `True` (_high_) or `False` (_low_).

    This pin must have previously been configured using a call to `setup_output_on_pin()`.
    """
    wpi.digitalWrite(pin_index, 1 if value else 0) # 0=low, 1=high


def query_input_pin(pin_index):
    """
    Query the input value of the given `pin_index`. This function returns `True` if the
    value of the pin is _high_, and it returns `False` if the value of the pin is _low_.

    This pin must have previously been configured using a call to `setup_input_on_pin()`.
    """
    return wpi.digitalRead(pin_index) == 1


def read_pin_pwm_value(pin_index):
    """
    Read the input from `pin_index` and return the PWM value in the
    range [0, 100].
    """

    while not query_input_pin(pin_index):
        pass
    while query_input_pin(pin_index):
        pass

    # BEGIN CYCLE AT _LOW_
    a = query_micros()

    while not query_input_pin(pin_index):
        pass

    # IS HIGH NOW
    b = query_micros()

    while query_input_pin(pin_index):
        pass

    # IS LOW NOW
    c = query_micros()

    return ((c - b) / (c - a)) * 100.


def delay_micros(num_microseconds):
    """
    Have the calling thread sleep for `num_microseconds` microseconds.
    There are 1000000 microseconds in a second.
    """
    wpi.delayMicroseconds(num_microseconds)


def query_micros():
    """
    Return a timestamp in microseconds.
    """
    return wpi.micros()

