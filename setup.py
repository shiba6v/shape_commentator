from setuptools import setup
import os
import subprocess
import io

VERSION = "0.6.3"

this_directory = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shape_commentator",
    packages=["shape_commentator"],
    version=VERSION,
    description="You can easily add numpy.ndarray.shape information to your script as comments.",
    author="shiba6v",
    author_email="shiba6v@gmail.com",
    url="https://github.com/shiba6v/shape_commentator",
    license="MIT",
    keywords=["numpy", "ndarray", "shape comment", "tool"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    entry_points={
        "console_scripts": [
        ]
    }
)
