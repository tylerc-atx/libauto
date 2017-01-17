import wiringpi as wpi
import time
import os


TRIG = 27
ECHO = 17


os.environ['WIRINGPI_GPIOMEM'] = "1"
import wiringpi as wpi
wpi.wiringPiSetupGpio()

wpi.pinMode(TRIG, 1)  # 0=input, 1=output 2=PWM
wpi.pinMode(ECHO, 0)  # 0=input, 1=output 2=PWM

wpi.digitalWrite(TRIG, 0) # 0=low, 1=high
wpi.delayMicroseconds(100000)  # 0.1 seconds


def get_echo_micros():

    wpi.digitalWrite(TRIG, 1) # 0=low, 1=high
    wpi.delayMicroseconds(10)
    wpi.digitalWrite(TRIG, 0) # 0=low, 1=high

    while wpi.digitalRead(ECHO) == 0:
        pass

    start = wpi.micros()

    while wpi.digitalRead(ECHO) == 1:
        pass

    end = wpi.micros()

    return end - start


def compute_distance_meters(echo_micros):

    distance_meters = echo_micros * 0.0003432
    return distance_meters


def compute_distance_feet(echo_micros):

    distance_feet = compute_distance_meters(echo_micros) * 3.28084
    return distance_feet


while True:
    echo_micros = get_echo_micros()
    print("meters = {}".format(compute_distance_meters(echo_micros)))
    print("feet   = {}\n".format(compute_distance_feet(echo_micros)))
    time.sleep(0.1)

