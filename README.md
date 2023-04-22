# Welcome to the MimicDB project


### A python virtualenv & requirements

Setup a python virtualenv.
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

```bash
pip install -r testing-requirements.txt
cd mimic
python manage.py test
```
