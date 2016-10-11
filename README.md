# data-group-service
[![Build Status](https://travis-ci.org/findexchange/data-group-service.svg?branch=master)](https://travis-ci.org/findexchange/data-group-service)
## Start service

In the project's folder run:
```
docker-compose up -d
```

Input data format
```
curl --data "data=[{\"_id\": \"stringIdOfRow1\", \"name\": \"Post Office Trafalgar Square\", \"town\": \"London\"}, {\"_id\": \"stringIdOfRow2\", \"name\": \"Post Office\", \"town\": \"London\"}, {\"_id\": \"stringIdOfRow3\", \"name\": \"Post Office\", \"town\": \"London\"}, {\"_id\": \"stringIdOfRow4\", \"name\": \"Post Office\", \"town\": \"London\"}, {\"_id\": \"stringIdOfRow5\", \"name\": \"Post Office\", \"town\": \"London\"}]" http://127.0.0.1:5000/api/v1.0/datasort
```
Expected output format

```
[
     {
         "name": "Post Office", 
         "count": 34443, 
         "rows": [
               "stringIdOfRow1", 
               "stringIdOfRow2", 
               ...
         ]
    },
    ...
]

```
