echo 'Deployment starting....'
which python
sudo apt-get install python3.9
pip install -r requirements.txt
python3.9 manage.py collectstatic
