from setuptools import setup
import os
import subprocess
import io

VERSION = "0.6.2"

def get_test_version():
    import requests
    import lxml.html
    url = "https://test.pypi.org/project/shape-commentator/"
    response = requests.get(url)
    html = lxml.html.fromstring(response.content)
    version_test = html.xpath("//*[@id='history']/section/div/a/p[1]")[0].text.strip()
    return version_test

# Check $TEST_RELEASE_HASH to confirm that this is TEST release. (Pass when it is PyPI release.)
# Add postN number to release test version.
if "TESTPYPI_PASSWORD" in os.environ:
    GIT_HASH = subprocess.check_output("git rev-parse --short HEAD".split()).strip().decode()
    if "TEST_RELEASE_HASH" in os.environ and\
        os.environ["TEST_RELEASE_HASH"] == GIT_HASH:
        previous_version = get_test_version().split(".post")
        if previous_version[0] != VERSION:
            # If version was updated, upload to TestPyPI without postN version.
            pass
        elif len(previous_version) != 2:
            # If previous version was non-postN version, add post-N.
            VERSION += ".post0"
        else:
            # Increment post release version number.
            VERSION += ".post" + str(int(previous_version[1])+1)

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
