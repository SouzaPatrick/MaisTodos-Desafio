## Start project with venv
I recommend creating a venv to install all the libs needed for the code to run and not have conflicts with the ones you already have on your PC

##### Create a venv with the command below
```bash
python -m venv venv
```
##### Activate the venv you just created
```bash
source venv/bin/activate
```
##### Install the necessary libs
```bash
pip install -r requirements/dev-requirements.txt
```
##### Populate the database
```bash
make generate_db

DB successfully reset
Create user test: 'username'='maistodos' 'password'='maistodos'
Authentication through Basic Auth
```
Just below the command to populate the database there is a list of everything that was done, it also indicates the username and password of the user to be used in your tests

##### Start Flask
```bash
gunicorn -w 3 -t 60 -b 0.0.0.0:5000 wsgi:app
```
###### Or you can boot in debug mode
```bash
python wsgi.py
```