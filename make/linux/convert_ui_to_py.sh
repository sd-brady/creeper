#!/bin/bash

# This script assumes that you are in a virtual environment with PyQt5 installed

# Generate Python file from the designer ui_main.ui file
script_directory=$(dirname "$(readlink -f "$0")")
pyuic5 -x $script_directory/../../src/frontend/designer/ui_main.ui -o $script_directory/../../src/frontend/modules/ui_main.py
