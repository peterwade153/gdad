# gdad
who is my granddaddy, a family tree search website

The Backend REST API is built with Python, Django, Django rest framework, and Uses PostgreSQL database.

## Local Set Up
The App has been set up with Docker and requires a local Docker installation.

To start the app

```docker compose up```

To seed the family tree data

```docker compose exec backend python manage.py seed```

## Tests
To run tests

```docker compose exec backend python manage.py test```

## Access App
```http://localhost:5173/```


