**Project**: A simple shop api

**Description**: Exposes a simple shop API for managing customers and their orders

## Getting Started

git clone the repo

### Prerequisites

docker and docker-compose
python

## Running the app

cd into the root of django_shop folder (where manage.py is located)

```python
cd django_shop/
```

Create a virtual environment

```python
$ python -m venv venv
```

activate the virtual environment

```python
$ source venv/bin/activate (linux environment)
```

Run the command to install all requirements from requirements.txt

```python
pip install -r requrements.txt
```

create a `.env` file in the `django_shop` settings folder (where `settings.py` is located)

update the `DATABASE_URL` environment variable following format in `env.template` file.

start the docker container with postgresql database

```bash
docker-compose -f build/docker-compose-dev.yml up
```

run database migrations

```python
python manage.py migrate
```

run the application by starting the server

```python
python manage.py runserver
```

## Author

- **Eugenia Mbuya**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
