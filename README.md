# Shape Commentator
[![CircleCI](https://circleci.com/gh/shiba6v/shape_commentator.svg?style=svg)](https://circleci.com/gh/shiba6v/shape_commentator)

## About  
You can easily add numpy.ndarray.shape information to your script as comments.

## Installation  
```bash
pip install shape_commentator
```

### Tested Python Version  
Test script must be written in these version of Python.
- 3.6.6
- 3.5.6
- 3.4.9
- 2.7.15

## Usage  
### CLI
1. Run this script as a module with argument of script name.  Command line arguments to the target script are available.

`python -m shape_commentator src.py`

`python -m shape_commentator src.py arg1 arg2`

2. You get the commented script. For example, you execute shape_commentator to `src.py`, you get `src.py.commented.py`.  
![src](https://user-images.githubusercontent.com/13820488/49359824-a4bf2200-f71a-11e8-93f2-b1d916e9cf3b.PNG)  
![src_commented](https://user-images.githubusercontent.com/13820488/49359827-a688e580-f71a-11e8-9e15-9ee509aca238.PNG)   

### IPython / Jupyter Notebook  
1. Execute the cell that you want to see shape.  
2. Run the cell below, and the commented source code will be outputted.  
```python
import shape_commentator
shape_commentator.comment(In[len(In)-2],globals(),locals())
```  
![jupyter](https://user-images.githubusercontent.com/13820488/49359830-a852a900-f71a-11e8-89b8-1c7b9ea17343.PNG)  

## Development  
### Python Main Version in Development  
- 3.6.6

### Prerequisities
```
pip install numpy
sudo apt install bats
```

### Test  
```
python -m doctest shape_commentator/shape_commentator.py
bats tests/test_all.bats
```

### Sample
```
python shape_commentator/shape_commentator.py tests/input_scripts/numpy_compute.py
```