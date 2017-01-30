# The following tells wiringpi to open /dev/gpiomem instead of /dev/mem.
os.environ['WIRINGPI_GPIOMEM'] = "1"

import wiringpi as wpi

# The following init method doesn't need root, but it
# is a very limited interface.
#wpi.wiringPiSetupSys()

# The following init method either needs root,
#   -- OR --
# it needs you to be in the `gpio` group and have set
# the WIRINGPI_GPIOMEM environment variable above.
wpi.wiringPiSetupGpio()


# The PWM range is related to the frequency, somehow.
# See the comments in:
#   https://projects.drogon.net/raspberry-pi/wiringpi/software-pwm-library/
PWM_RANGE = 100


def setup_pwm_on_pin(pin_index):
    wpi.pinMode(pin_index, 1)  # 0=input, 1=output, 2=hardPWM
    wpi.softPwmCreate(pin_index, 0, PWM_RANGE)


def set_pin_pwm_value(pin_index, value):
    value = int(value / 100.0 * PWM_RANGE)
    wpi.softPwmWrite(pin_index, value)


def setup_output_on_pin(pin_index):
    wpi.pinMode(pin_index, 1)  # 0=input, 1=output, 2=hardPWM


def set_output_pin_value(pin_index value):
    wpi.digitalWrite(pin_index, 1 if value else 0) # 0=low, 1=high


def setup_input_on_pin(pin_index):
    wpi.pinMode(pin_index, 0)  # 0=input, 1=output, 2=hardPWM


def query_input_pin(pin_index):
    return wpi.digitalRead(ECHO) == 1


def delay_micros(num_microseconds):
    wpi.delayMicroseconds(num_microseconds)


def query_micros():
    return wpi.micros()

