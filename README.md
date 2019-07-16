# Shape Commentator
[![CircleCI](https://circleci.com/gh/shiba6v/shape_commentator.svg?style=svg)](https://circleci.com/gh/shiba6v/shape_commentator)

## About  
You can easily add numpy.ndarray.shape, torch.Size, other "shape" and type information to your script as comments.

![Sample](https://user-images.githubusercontent.com/13820488/50560224-e656e300-0d41-11e9-90a3-f946cb40ab72.png)

An article about this tool is here. (in Japanese)
[NumPyやPyTorchで使える超便利ツールを作った](http://shiba6v.hatenablog.com/entry/shape_commentator_release)

## Getting Started  
### For Jupyter Notebook User
[This](https://github.com/shiba6v/jupyter-shape-commentator) is a Jupyter Notebook extension of this tool. It is easier to use!

![use_fig](https://user-images.githubusercontent.com/13820488/61187795-fcf6d300-a6b0-11e9-97c6-4fd029244839.png)

### NumPy
```bash
pip install shape_commentator numpy
echo -e "import numpy as np\na = np.array([1,2,3])" > src.py
python -m shape_commentator src.py
cat src.py.commented.py
```

```python
import numpy as np
a = np.array([1,2,3])  #_ (3,)

```

### PyTorch
```bash
pip install shape_commentator torch
echo -e "import torch\na = torch.tensor([1,2,3])" > src.py
python -m shape_commentator src.py
cat src.py.commented.py
```

```python
import torch
a = torch.tensor([1,2,3])  #_ torch.Size([3])

```

## Table Of Contents
- [Shape Commentator](#shape-commentator)
  * [About](#about)
  * [Getting Started](#getting-started)
    + [NumPy](#numpy)
    + [PyTorch](#pytorch)
  * [Usage](#usage)
    + [Execute as a Module](#execute-as-a-module)
      - [Create Commented Script to File](#create-commented-script-to-file)
      - [Create Commented Script to Standard Output](#create-commented-script-to-standard-output)
      - [Clear Shape Comment](#clear-shape-comment)
    + [IPython / Jupyter Notebook](#ipython---jupyter-notebook)
      - [Create Commented Script](#create-commented-script)
      - [Clear Shape Comment](#clear-shape-comment-1)
  * [Tested Python Version](#tested-python-version)
  * [Development](#development)
    + [Python Main Version in Development](#python-main-version-in-development)
    + [Installation](#installation)
    + [Sample](#sample)
    + [Test](#test)
    + [Changing Test Scripts](#changing-test-scripts)
    + [Try Master Branch](#try-master-branch)
  * [Further Reading](#further-reading)

## Usage  
### Execute as a Module
#### Create Commented Script to File
1. Run this script as a module with argument of script name.  Command line arguments to the target script are available.

```bash
python -m shape_commentator src.py [args]
```

2. You get the commented script. For example, you execute shape_commentator to `src.py`, you get `src.py.commented.py`.  

`src.py`
```python
import numpy as np
a = np.array([1,2,3,4,5,6])
b = np.array([0,1,2,3,4,5])
ab_h = np.hstack((a,b))
ab_v = np.vstack((a,b))
ab = np.dot(a,b)
AA, BB = np.meshgrid(a,b)
i = 1
f = 1.0
c = 1 + 1j
s = "string1"
class A():
    pass
a = A()
```

`src.py.commented.py`
```python
import numpy as np
a = np.array([1,2,3,4,5,6])  #_ (6,)
b = np.array([0,1,2,3,4,5])  #_ (6,)
ab_h = np.hstack((a,b))  #_ (12,)
ab_v = np.vstack((a,b))  #_ (2, 6)
ab = np.dot(a,b)  #_ ()
AA, BB = np.meshgrid(a,b)  #_ [(6, 6),(6, 6),]
i = 1  #_ int
f = 1.0  #_ float
c = 1 + 1j  #_ complex
s = "string1"  #_ str
class A():
    pass
a = A()  #_ A
```

#### Create Commented Script to Standard Output
By using `shape_commentator.print_comment` module, you get the commented script in standard output. (Not `src.py.commented.py`)
```bash
python -m shape_commentator.print_comment src.py [args]
```

#### Clear Shape Comment
By using `shape_commentator.print_clear` module, you get the uncommented script in standard output.
```bash
python -m shape_commentator.print_clear src.py [args]
```

### Jupyter Notebook  
Jupyter Notebook Extension is [HERE](https://github.com/shiba6v/jupyter-shape-commentator)

### IPython
#### Create Commented Script
1. Execute the cell that you want to see shape.  
2. Run the cell below, and the commented source code will be outputted.  (`In[len(In)-2]` is the source code in the cell that you ran just before.)

```python
import shape_commentator
shape_commentator.comment(In[len(In)-2],globals())
```  
![ipython_comment](https://user-images.githubusercontent.com/13820488/50559871-1ac8a000-0d3e-11e9-923e-997f6aac6d68.png)  

#### Clear Shape Comment
```python
import shape_commentator
shape_commentator.clear(In[len(In)-2])
```  
![ipython_clear](https://user-images.githubusercontent.com/13820488/50559879-37fd6e80-0d3e-11e9-8c06-7f6963396dcb.png)  

## Tested Python Version  
Test script must be written in these version of Python.
- 3.6.6
- 3.5.6
- 3.4.9
- 2.7.15

## Development  
### Python Main Version in Development  
- 3.6.6

### Installation
```
pip install numpy
sudo apt install bats
sh tests/install_for_dev.sh
```

### Sample
```
# Module Mode
python -m shape_commentator tests/input_scripts/numpy_compute.py
# Method Mode (Use in IPython / Jupyter Notebook.)
python tests/comment_method.py tests/input_scripts/numpy_compute.py 
```

### Test  
```
python -m doctest shape_commentator/shape_commentator.py
sh tests/install_for_dev.sh
bats tests/test_all.bats
python setup.py develop --uninstall
```

### Changing Test Scripts
Remove `remove_tested_scripts` in `tests/test_all.bats` and run `bats tests/test_all.bats`, and you get new test script in `tests/input_scripts/`

### Try Master Branch
The package of shape_commentator in TestPyPI is the HEAD of master branch.  
You can try newest (but under development) version by running commands below.
```
pip uninstall -y shape-commentator
pip install --index-url https://test.pypi.org/simple/ shape-commentator
```
