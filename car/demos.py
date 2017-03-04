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
This module contains solutions to many of the AutoAuto labs. These make it
easy for the instructor to show demos of the labs.
"""


def lab1():
    """
    Demo the car driving in all four possible directions.
    """
    import car

    car.left()
    car.right()
    car.reverse()
    car.forward()


def lab2():
    """
    Demo the car driving in a figure-8.
    """
    import car

    car.right()
    car.right()
    car.left()
    car.left()


def lab3():
    """
    Demo nothing! Lab 3 has no demo.
    """
    pass


def lab4(distance_limit = 0.2, forward_step_time=0.15, sleep_time=0.3):
    """
    Demo the car avoiding obstacles using only the sonar sensor.
    """
    import car
    from car import sonar
    import random
    import time

    try:

        while True:

            current_distance = sonar.query_distance()

            while current_distance > distance_limit:
                car.forward(forward_step_time)
                time.sleep(sleep_time)
                current_distance = sonar.query_distance()

            car.reverse()

            if random.choice([True, False]):
                car.right()
            else:
                car.left()

    except KeyboardInterrupt:

        print("Quitting...")

