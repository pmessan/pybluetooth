from setuptools import find_packages, setup

setup(
    name="pybluetooth",
    packages=find_packages(include=["pybluetooth"]),
    version="0.1.0",
    description="A Python library to connect with Bluetooth devices on the terminal.",
    author="Peter-Newman Messan",
    license="MIT",
    install_requires=["pybluez"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
