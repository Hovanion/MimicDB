# Welcome to the MimicDB project

## Installation

This is the best I can do for documentation to get **mimicDB** up and running.
Unfortunately something still seems to be going wrong (most likely SQLite
related), but these instructions *should* be the "right way" to get the
development enviroment up and running...

### A python virtualenv & requirements

Setup a python virtualenv, I think any version of python 3 should work. I hope
you know how to setup a python virtualenv, if not, let me know. 

Next, install the requirements (and testing requirements):

```bash
pip install -r requirements.txt
```

### Database 

The `rebuild.sh` script *should* rebuild the entire database, and should simpy work like this:

```bash
cd mimic 
./rebuild.sh
```

But if it doesn't work, its worthwhile trying running the steps in the script by hand. Just some notes:

* **mimicDB** uses an SQLite database, and **django** migrations to craete the right structure.
* You can safely remove the database file *db.sqlite3*, nothing important is stored there...
* Run `python manage.py migrate` to rebuild the database structure
* The data is loaded (step by step) from the files in the *data* folder

### Deploy

If I remember correctly the development server can be launched with:

```bash
cd mimic
python manage.py runserver
```

### Testing

At some point, there working tests for the project (neat right!). Something like the following *should* be enough to run the tests:

```bash
pip install -r testing-requirements.txt
cd mimic
python manage.py test
```
