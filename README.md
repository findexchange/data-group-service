# data-group-service
[![Build Status](https://travis-ci.org/findexchange/data-group-service.svg?branch=master)](https://travis-ci.org/findexchange/data-group-service)
## Start service

In the project's folder first need to compile ```clusterng.pyx```, run:
```
python setup.py build_ext -i
```
then run:
```
docker-compose up -d
```

Input data format
```
curl --data "data=[
                   {\"_id\": \"stringIdOfRow1\", \"name\": \"Post Office Trafalgar Square\", \"town\": \"London\"},
                   {\"_id\": \"stringIdOfRow2\", \"name\": \"Post Office\", \"town\": \"London\"},
                   {\"_id\": \"stringIdOfRow3\", \"name\": \"Post Office\", \"town\": \"London\"}, 
                   {\"_id\": \"stringIdOfRow4\", \"name\": \"Post Office\", \"town\": \"London\"},
                   {\"_id\": \"stringIdOfRow5\", \"name\": \"Post Office\", \"town\": \"London\"}
                   ]" 
http://127.0.0.1:5000/api/v1.0/datasort
```
Expected output format,
if success:

```
{
    "results": [
      {
        "count": 5,
        "groupName_Id": 0,
        "rows": [
                "stringIdOfRow1",
                "stringIdOfRow2",
                "stringIdOfRow3",
                "stringIdOfRow4",
                "stringIdOfRow5"
                ],
        "tags": "post office"
      }
    ],
    "status": "success"
}

```
if error:

```
{
      "error": "string indices must be integers, not str",
      "status": "error"
}
```
