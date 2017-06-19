# libauto

The Python library for all AutoAuto devices

# Examples

Run these examples on a real car.

### Calibrate the Throttle and Steering

```python
from car.setup import calibrate

calibrate()
```

### Drive the Car!

```python
import car

car.forward()
car.left()
car.right()
car.reverse()
car.pause(2.0)
car.forward(0.2)
```

### Print to the AutoAuto Console!

```python
import car

car.print("Hello, my friend!")
car.print("How are you today?")
```

### Use the Camera

```python
import car

frames = car.capture(4)
car.plot(frames)

# There is also a lower-level class-based interface for the camera: `from car.camera import CameraRGB`
```

### Detect Humans

```python
import car

frame = car.capture()
car.detect_faces(frame)
car.plot(frame)

# There is also a lower-level class-based interface for the face detector: `from car.models import FaceDetector`
```

### Stream Camera Frames (and detect humans)

The frames can be viewed at http://ip-of-your-car:1025/

```python
import car

for _ in range(1000):
    frame = car.capture(verbose=False)
    car.detect_faces(frame)
    car.stream(frame)
```

### Classify Frame Center Color

```python
import car

frame = car.capture()
color = car.classify_color(frame)
car.plot(frame)
car.print("The detected color is", color)

# There is also a lower-level class-based interface for the color classifier: `from car.models import ColorClassifier`
```

### Detect Stop Signs

```python
import car

frame = car.capture()
rectangles = detect_stop_signs(frame)
car.plot(frame)
print("Stop Signs Found at:", rectangles)

# There is also a lower-level class-based interface for the stop sign detector: `from car.models import StopSignDetector`
```

### Detect Pedestrians

```python
import car

frame = car.capture()
rectangles = detect_pedestrians(frame)
car.plot(frame)
print("Pedestrians Found at:", rectangles)

# There is also a lower-level class-based interface for the stop sign detector: `from car.models import PedestrianDetector`
```

### Object Location/Size Helpers

```python
import car

frame = car.capture()
rectangles = detect_stop_signs(frame)
car.plot(frame)

location = car.object_location(rectangles, frame.shape)
size = car.object_size(rectangles, frame.shape)

car.print("Object location:", location)
car.print("Object size:", size)
```

### Raw OpenCV

The cars use OpenCV under the hood (no pun intended) for many of the image processing tasks. You are welcome to use OpenCV directly as well if you want:

```python
import cv2

print(cv2.__version__)
```

### Precise Steering

```python
import car
from car.steering import set_steering

for angle in range(-45, 45):
    set_steering(angle)
    car.pause(0.05)
    
for angle in range(45, -45, -1):
    set_steering(angle)
    car.pause(0.05)
    
car.pause(0.5)
set_steering(0.0)  # STRAIGHT
car.pause(1.0)
```

### Precise Throttle

WARNING: You can easily injure the car by setting the throttle too high. Use this interface with great caution.

Run the code below in a large open space.

```python
import car
from car.throttle import set_throttle

set_throttle(0.0)     # CAR IN NEUTRAL
car.pause(1.0)

set_throttle(100.0)   # CAR'S MAX THROTTLE
car.pause(0.3)

set_throttle(50.0)    # HALF THROTTLE
car.pause(0.5)

set_throttle(0.0)     # NEUTRAL
car.pause(2.0)
```

### Sonar Sensor (if available and working properly)

```python
from car.sonar import echo_time, query_distance

seconds = echo_time()
print("It took {} seconds for the ping to travel round-trip.".format(seconds))

distance_meters = query_distance()
print("The estimated distance to the nearest object is {} meters.".format(distance_meters))
```

### Radio-Controlled (RC) Car Mode

You can return your car to it's original state: A basic RC car! This only works if your AutoAuto car has a receiver on it, and if you have a paird transmitter.

```python
from car.rc import manual_control

manual_control()
```

### Low-level GPIO

You can get access to the raw GPIO pins via the `car.gpio` module.

# How to run in an Anaconda environment

You can run some things off the car (on your local machine). Get a matching python environment like this:
```bash
conda create -n py3 scikit-learn matplotlib jupyter python=3.4
source activate py3
conda install -c https://conda.binstar.org/menpo opencv3
pip install keras
pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.0.0-py3-none-any.whl
rm -f ~/.keras/keras.json
conda install requests h5py pandas twisted openssl
```
