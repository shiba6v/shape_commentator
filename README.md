# Shape Commentator
[![CircleCI](https://circleci.com/gh/shiba6v/shape_commentator.svg?style=svg)](https://circleci.com/gh/shiba6v/shape_commentator)

## About  
You can easily add numpy.ndarray.shape, torch.Size, other shape and type information at runtime to your script as comments.

NumPyやPyTorchなどの配列のshape属性や，変数の型の実行時の情報を，ソースコードにコメントとして貼り付けるツールです．

![Sample](https://user-images.githubusercontent.com/13820488/70534467-76321d80-1b9e-11ea-9ff1-e2d9c4140382.png)

## Usage  
### Execute as a Module
#### Create Commented Script to File
1. Run this script as a module with argument of script name.  Command line arguments to the target script are available.

Pythonのモジュールとしてshape_commentatorを実行してください．引数は，スクリプト名の後にスクリプトに渡したい引数を続けてください．

```bash
python -m shape_commentator src.py
```

```bash
python -m shape_commentator src.py arg1 arg2 arg3
```

2. You get the commented script. For example, you execute shape_commentator to `src.py`, you get `src.py.commented.py`.  

`src.py`というスクリプトに対して実行すると，`src.py.commented.py`が生成されます．

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

### IPython / Jupyter Notebook (Magic Command)
To use IPython magic command,

IPythonでのマジックコマンドの使い方
```python
import shape_commentator
```

#### Create Commented Script
コメントを付ける
```python
%%shape
a = np.array([1,2,3,4,5,6])
```

output
```
a = np.array([1,2,3,4,5,6])  #_ (6,)
```

#### Delete Comments
コメントを消す
```python
%%shape -d
a = np.array([1,2,3,4,5,6])  #_ (6,)
```

output
```
a = np.array([1,2,3,4,5,6])
```

## Tested Python Version  
Test scripts are written in these version of Python.
以下のバージョンがテストされています．
- 3.8.0
- 3.7.5
- 3.6.9
- 3.5.9
- 3.4.10
- 2.7.17

## Blog
作った経緯などを書いた解説ブログはこちらにあります．
[NumPyやPyTorchで使える超便利ツールを作った](http://shiba6v.hatenablog.com/entry/shape_commentator_release)
