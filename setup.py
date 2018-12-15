from setuptools import setup

setup(
    name="shape_commentator",
    packages=["shape_commentator"],
    version="0.1.4",
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