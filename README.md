# System requirements
* python (approved version ```3.6.6```)
* pip
* virtualenv
* mysql (approved version ```8.0.13```)

# Installation steps
* Clone github repo into any directory you like
* Create your own virtual environment via ``` virtualenv dev ```
* Activate it by ``` source dev/bin/activate ``` for *mac/linux* users, ``` dev\Scripts\activate ``` for *Windows*
* Install project depencies ``` pip install -r requirements.txt ```
* Specify your own db creds int `aircompany.ini` file
* If you wanna run application in DEBUG mode type ```export FLASK_DEBUG=1``` for *mac/linux* or ``` set FLASK_DEBUG=1 ``` for *Windows* (traces on pages will be avaiable)
* Initialize db via ```flask db upgrade```
* Specify your app name in FLASK_APP var, ```export FLASK_APP=aircompany.py``` for *mac/linux* or ``` set FLASK_APP=aircompany.py ``` for *Windows*
* run server ```flask run```


site will be avaiable at ```0.0.0.0:5000/```


Example of ```aircompany.ini```
```bash
[config]
dbname=
dbpassword=
dbhost=
dbuser=
secret_key=
sqlalchemy_track_modifications=
user_mail_sender_email=
```