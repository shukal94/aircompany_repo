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
* If you wanna run application in DEBUG mode type ```export FLASK_DEBUG=1 / export FLASK_ENV=development``` for *mac/linux* or ``` set FLASK_DEBUG=1 / set FLASK_ENV=development``` for *Windows* (traces on pages will be avaiable)
* Specify your app name in FLASK_APP var, ```export FLASK_APP=aircompany.py``` for *mac/linux* or ``` set FLASK_APP=aircompany.py ``` for *Windows*
* Initialize db via ```flask db init && flask db upgrade```
* run server ```flask run```


site will be avaiable at ```0.0.0.0:5000/```


Example of ```aircompany.ini```
```bash
[config]
dbname=
dbpassword=
dbhost=
dbuser=
secret_key=youllneverguess
sqlalchemy_track_modifications=False
user_mail_sender_email=noreply@air.com
```

## Probable issues
sometimes someone push several changes in db, sometimes it kind of hurt
* when you try to ```flask db migrate -m "some change""``` (or update db after migration) alembic will say: No, I couldnt add/delete/update table field
No worries, just check attentively your migration files and running instance of db
* the second one when alembic try to get revision hash that doesnt exists, just drop ```alembic_version``` in your db and remove ```migrations``` dir
then ```flask db init && flask db migrate -m "again" && flask db upgrade```

