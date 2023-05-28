## Other Usage  
The main usage are described in `README.md`.

### For Editor Extension Developers
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

### For Jupyter Notebook User (deprecated)
[This](https://github.com/shiba6v/jupyter-shape-commentator) is a Jupyter Notebook extension of this tool. 
It is deprecated now. Please use IPython extension.

![use_fig](https://user-images.githubusercontent.com/13820488/61187795-fcf6d300-a6b0-11e9-97c6-4fd029244839.png)

### IPython (Cell)
#### Create Commented Script
1. Execute the cell that you want to see shape.  
2. Run the cell below, and the commented source code will be outputted.  (`In[len(In)-2]` is the source code in the cell that you ran just before.)

```python
import shape_commentator
shape_commentator.comment()
```  
![ipython_comment](https://user-images.githubusercontent.com/13820488/50559871-1ac8a000-0d3e-11e9-923e-997f6aac6d68.png)  

#### Clear Shape Comment
```python
import shape_commentator
shape_commentator.clear()
```  
![ipython_clear](https://user-images.githubusercontent.com/13820488/50559879-37fd6e80-0d3e-11e9-8c06-7f6963396dcb.png)  

### Formatting comments used in Shape Commentator
This tool emits very long shape comment.
```python
import shape_commentator.formatter as fmt
code = [i for i in range(1000)]
print(fmt.tuple_format(code))
```

output
```
[int,int,int,int,int,int,int,int,int, ... ]
```

## Development  
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
