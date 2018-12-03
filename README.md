# Shape Commentator

## About
You can easily add numpy.ndarray.shape to your script as comment.


## Usage
### CLI
1. Run this script as a module with argument of script name.  Command line arguments to the target script are available.

`python -m shape_commentator src.py`

`python -m shape_commentator src.py arg1 arg2`

2. You get the commented script. For example, you execute shape_commentator to `src.py`, you get `src.py.commented.py`.

### Jupyter
1. Execute the cell that you want to see shape.
2. Run the cell below, and the commented source code will be outputted.
```python
import shape_commentator
shape_commentator.comment(In[len(In)-2],globals(),locals())
```
