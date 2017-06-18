# libauto

The Python library for all AutoAuto devices

# Examples

Run these examples on a real car.

### Calibrate the Throttle and Steering

```python
from car.setup import calibrate
calibrate()
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
