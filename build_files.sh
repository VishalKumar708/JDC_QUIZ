# Update package manager and install Python 3.9
sudo apt-get update
sudo apt-get install python3.9 python3.9-distutils

# Install pip for Python 3.9
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

# Install project dependencies
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput
