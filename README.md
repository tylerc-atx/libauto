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
```

### Detect Humans

```python
import car

frame = car.capture()
car.detect_faces(frame)
car.plot(frame)
```

### Stream Camera Frames (and detect humans)

The frames can be viewed at http://ip_of_your_car:1025/

```python
import car

while True:
    frame = car.capture()
    car.detect_faces(frame)
    car.stream(frame)
```

### Detect Frame Center Color

```python
import car

frame = car.capture()
color = car.classify_color(frame)
car.plot(frame)
car.print("The detected color is", color)
```

### Detect Stop Signs

```python
import car

frame = car.capture()
rectangles = detect_stop_signs(frame)
car.plot(frame)
print("Stop Signs Found at:", rectangles)
```

### Detect Pedestrians

```python
import car

frame = car.capture()
rectangles = detect_pedestrians(frame)
car.plot(frame)
print("Pedestrians Found at:", rectangles)
```

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
