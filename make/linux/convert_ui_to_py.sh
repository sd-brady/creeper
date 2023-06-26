#!/bin/bash

# This script assumes that you are in a virtual environment with PyQt5 installed

# Generate Python file from the designer ui_main.ui file
pyuic5 -x ../../src/frontend/designer/ui_main.ui -o ../../src/frontend/modules/ui_main.py
