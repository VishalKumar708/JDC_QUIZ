#!/bin/bash

# Install pip if not already installed
echo "deployment execution start...."
if ! command -v pip &>/dev/null; then
    echo "Installing pip..."
    sudo apt-get install python3-pip
fi

# Locate Python Path
python_path=$(which python3.9)
echo "Python Path: $python_path"

# Install Django
$python_path -m pip install django

# Install project dependencies from requirements.txt
$python_path -m pip install -r requirements.txt

# Collect static files (for Django projects)
$python_path manage.py collectstatic

