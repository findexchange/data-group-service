# data-group-service
[![Build Status](https://travis-ci.org/findexchange/data-group-service.svg?branch=master)](https://travis-ci.org/findexchange/data-group-service)
## Start service

In the project's folder run:
```
docker-compose up -d
```

Input data format
```curl --data "data=[{\"_id\": \"stringIdOfRow1\", \"name\": \"Post Office Trafalgar Square\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow2\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow3\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow4\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow5\", \"name\": \"Post Office\", \"postal_town\": \"London\"}]" http://127.0.0.1:5000/api/v1.0/datasort
```
or without ```"data=```
```
curl --data "[{\"_id\": \"stringIdOfRow1\", \"name\": \"Post Office Trafalgar Square\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow2\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow3\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow4\", \"name\": \"Post Office\", \"postal_town\": \"London\"}, {\"_id\": \"stringIdOfRow5\", \"name\": \"Post Office\", \"postal_town\": \"London\"}]" http://127.0.0.1:5000/api/v1.0/datasort

```