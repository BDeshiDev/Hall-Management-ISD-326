# Hall-Management-ISD-326
## Exporting current DB data:
```
python manage.py dumpdata --format "xml" > "fixture.xml"
```
* Django seems to mess up encoding, after dumping, open in notepad and save as and overwrite wit utf-8 as encoding
* alternatively, edit the fixture file’s first line to user utf-16
* `<?xml version="1.0" encoding="utf-16"?>`
    
    
## loading exported data
```
python manage.py loaddata "fixture.xml"
````

## loading exported data
```
python manage.py loaddata "fixture.xml"
````
## Resetting DB
```
python manage.py flush
```
