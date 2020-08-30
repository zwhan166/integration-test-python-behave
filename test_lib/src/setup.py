from setuptools import setup, find_packages

setup(
    name="sogeti_test_lib",
    version="0.0.1",
    packages=find_packages(),
    
    install_requires=[
        "behave>=1.2.6",
        "PyHamcrest>=2.0.2",
        "selenium>=3.141.0",
        "requests>=2.24.0",
    ],
    
    author="Zhengwei Han",
    author_email="zw.han@hotmail.com",
    description="Sogeti test library"
)
