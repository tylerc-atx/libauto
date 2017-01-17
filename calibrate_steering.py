import car
import time

while True:

    smin = float(input("Steering min: "))
    smid = float(input("Steering mid: "))
    smax = float(input("Steering max: "))

    car.calibrate_steering(smin, smid, smax)

    if input("Keep? ") == 'y':
        break
