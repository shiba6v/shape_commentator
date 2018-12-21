from setuptools import setup
import os
import subprocess

VERSION = "0.1.4"

def get_test_version():
    import requests
    import lxml.html
    url = "https://test.pypi.org/project/shape-commentator/"
    response = requests.get(url)
    html = lxml.html.fromstring(response.content)
    version_test = html.xpath("//*[@id='history']/section/div/a/p[1]")[0].text.strip()
    return version_test

# $TEST_RELEASE_HASHで短いコミット番号を確認して，意図したバージョンのテストリリースであることを確認．
# TestPyPIでリリースバージョンが被ってCIがコケるのを防ぐためにdev番号を付与．
GIT_HASH = subprocess.check_output("git rev-parse --short HEAD".split()).strip().decode()
if "TESTPYPI_PASSWORD" in os.environ and\
    "TEST_RELEASE_HASH" in os.environ and\
    os.environ["TEST_RELEASE_HASH"] == GIT_HASH:
    previous_version = get_test_version().split(".dev")
    if previous_version[0] != VERSION:
        # マイナーバージョン以上のアップデートを入れた時は，devを付けずにテストリリース
        pass
    elif len(previous_version) != 2:
        # 直前が本リリースの時は，dev0としてテストリリース
        VERSION += ".dev0"
    else len(previous_version) == 2 and previous_version[0] == VERSION:
        # 直前にN.N.N.devNのテストリリースをTestPyPIで行った時に，dev(N+1)としてテストリリース．
        VERSION += ".dev" + str(int(previous_version[1])+1)

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
    long_description_content_type="text/markdown",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "shape_commentator = shape_commentator.shape_commentator:main"
        ]
    }
)