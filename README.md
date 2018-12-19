# Crawler and data analytics project

This project crawlers documents from IMDb website https://www.imdb.com/.

### Frameworks

Framework used in this project:

* [Python 3.6.5] - for the backend
* [Flask Framework] - python microframework
* [BeautifulSoup] - To crawler

### Docker

To run the application, it is necessary to perform the build of the docker compose,
since it's done, the application can already be executed with the compose up.

### mLab - MongoDB

The data is stored on mLab MongoDB services.

[Build] - Production environment

```sh
cd crawler-app
docker-compose build
```

[Build] - Development environment

```sh
cd crawler-app
docker-compose -f docker-compose.yml -f docker-compose-dev.yml build
```

[Run] - Production environment

```sh
cd crawler-app
docker-compose up
```

[Run] Development environment

```sh
cd crawler-app
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d
```

### Test
To test the application it is needed to follow these steps:

- Configure the Docker to run de App
- Run tests on the Docker prompt:

```sh
docker exec crawler_application python -m pytest --cov-report term-missing --cov . /app/tests
```