#!/bin/bash

# Locate Python Path
python_path=$(which python3.9)

# Install project dependencies from requirements.txt
$python_path -m pip install -r requirements.txt

# Collect static files (for Django projects)
$python_path manage.py collectstatic

