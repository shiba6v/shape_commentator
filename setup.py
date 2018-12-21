from setuptools import setup
import os
import subprocess

VERSION = "0.1.4"

# $TEST_RELEASE_HASHに短いコミット番号をつけると，テストリリース時にそれを後ろにつける．
# TestPyPIでリリースバージョンが被ってCIがコケるのを防ぐため．
GIT_HASH = subprocess.check_output("git rev-parse --short HEAD".split()).strip().decode()
if "TESTPYPI_PASSWORD" in os.environ and\
    "TEST_RELEASE_HASH" in os.environ and\
    os.environ["TEST_RELEASE_HASH"] == GIT_HASH:
    VERSION += "-" + GIT_HASH

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
    long_description=open("README.md").read(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "shape_commentator = shape_commentator.shape_commentator:main"
        ]
    }
)