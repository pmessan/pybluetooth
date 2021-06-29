# PyBluetooth Library

This repo contains a Python Library based on pygatt and pybluez, and is intended to identify bluetooth device through the terminal and establish connections with them to exchange data. The repo is structured as follows:

* pybluetooth/: folder housing functions.py, which contains the functions making calls to the pygatt and pybluez libraries to scan for nearby devices, as well as run a bluetooth server/client.
* tests/: a folder containing a few test cases for testing the scan(), client() and server() functions.

I created a setup.py as well in order to package the file into a library which can be installed locally with 
```python3 setup.py bdist_wheel ; pip install dist/pybluetooth-0.1.0-py3-none-any.whl```
After local installation, the files in the tests/ directory can be run successfully.
