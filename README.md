# Hall-Management-ISD-326
## Exporting current DB data:
```
python manage.py dumpdata --format "xml" > "fixture.xml"
```
* Django seems to mess up encoding, after dumping, open in notepad and save as and overwrite with utf-8 as encoding
* alternatively, edit the fixture file’s first line to use utf-16
* `<?xml version="1.0" encoding="utf-16"?>`
    
    
## loading exported data
```
python manage.py loaddata "fixture.xml"
```
## Resetting DB
```
python manage.py flush
```

## Views And Templates
template files are placed in _BASE/RoomAllotment/templates/RoomAllotment_ and images are kept in _BASE/static/image_

Allowed non-admin urls:
1. /
2. /login
3. /student/<std_id>
4. /provost/<prv_id>
5. /student/<std_id>/room-req
6. /provost/<prv_id>/room-allot
