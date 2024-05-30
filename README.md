# Painkiller Injection System

Welcome to the Painkiller Injection System project!

## Introduction

The Painkiller Injection System is a software project designed to automate the process of administering painkiller medication. The system is intended for use in healthcare settings where precise control over medication dosage is crucial.

The system works by interfacing with a hardware device that controls the delivery of the medication. The software allows healthcare professionals to set the dosage and administration schedule, and it automatically controls the device to deliver the medication according to the set schedule.

The software also includes safety features to prevent overdosing, such as maximum dosage limits and alerts for unusual administration patterns.

The project is implemented in Python and uses the tkinter library for the user interface. It also includes a suite of unit tests to ensure the software functions as expected.


## Usage

### Running the Main Program

To run the main program, execute the following command:
    python -m main

### Running Unit Tests

To run unit tests, use the following command:
    e.g for the `core` module
    python -m unittest project.tests.unit.test_core

To run all unit tests, execute:
    python -m unittest discover -s project/tests/unit

### Running Functional Tests

To run functional tests, execute:
    e.g for the `doctorAPP` module
    python -m unittest project.tests.functional.test_doctorAPP_functional

To run all unit tests, execute:
    python -m unittest discover -s project/tests/functional

### Running Specific Modules

To run a specific module, such as `doctorAPP`, use the following command:
    python -m project.src.doctorAPP



