# DTEAM-django-practical-test

### Load test data

```
poetry run python manage.py loaddata cv_data.json
```

### Run tests 

```
poetry run python manage.py test
```

### Configure .env file
```
DEBUG=True
ALLOWED_HOSTS=*

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

### Run docker container and load test data

```
docker-compose up -d
docker-compose exec web poetry run python manage.py loaddata cv_data.json
```