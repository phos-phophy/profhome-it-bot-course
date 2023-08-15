## Motivation

Try to design an application architecture that conforms to the following principles:

* DRY - Don't Repeat Yourself
* KISS - Keep It Simple, Stupid
* DI - Dependency Injection
* SOLID
  * S - Single Responsibility Principle, SRP
  * O - Open/Closed Principle, OCP
  * L - Liskov Substitution Principle, LSP
  * I - Interface Segregation Principle, ISP
  * D - Dependency Inversion Principle, DIP


## Description

A very simple template of FastAPI application that can be extended in the future. There are 3 endpoints:
* `POST /user/register` - registers new common (non-admin) user
* `POST /user/auth` - authenticates user and returns JWT session token
* `GET /users` - returns list of all common (non-admin) users

PostgreSQL is used as an application database.

This is my first experience of building a web application as well as using FastAPI, SQLAlchemy, Alembic and PostgresQL. I tried to make the
application secure and structured.


## How to start

```
usage: main.py [-h] [-c CONFIG] [-s SERVER_CONFIG]

Bot CLI arguments

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the app configuration file
  -s SERVER_CONFIG, --server_config SERVER_CONFIG
                        Path to the server configuration file
```

1. Run `openssl rand -hex 32` to generate your secret key that will be used to sign the JWT tokens.
   And copy the output to the environment variable `SECRET_KEY`.
    ```bash
    export SECRET_KEY=$(openssl rand -hex 32)
    ```
2. Configure PostgresQL server:
   1. To install and configure your own PostgresQL server, please refer to https://ubuntu.com/server/docs/databases-postgresql 
   (Installation and Configuration sections)

   2. Database URL has the following structure: `postgresql://<user>:<password>@<localhost>/<name_of_the_database>`. Save it to the
   `POSTGRESQL_URL` environment variable:
        ```bash
        export POSTGRESQL_URL=postgresql://<user>:<password>@<localhost>/<name_of_the_database>
        ```

3. Run `alembic revision --autogenerate -m "Init"` to generate init migration and `alembic upgrade head` to enable it.

4. Finally, run `python main.py [-h] [-c CONFIG] [-s SERVER_CONFIG]` to start application.


## Documentation

To check the automatic interactive API documentation, you can open your browser at 
http://127.0.0.1:8000/docs (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)) 
or go to http://127.0.0.1:8000/redoc (provided by [ReDoc](https://github.com/Redocly/redoc))

OpenAPI schema is available at http://127.0.0.1:8000/openapi.json

**NOTE:** 127.0.0.1 and 8000 are the default host and port respectively. If other values are used in your server configuration file, then 
your application is located at `http://{host}:{port}`

## Good resources
1. [Official FastAPI documentation](https://fastapi.tiangolo.com/)
2. [FastAPI Stepik course](https://stepik.org/course/179694/)
3. [Official SQLAlchemy 1.4 documentation](https://docs.sqlalchemy.org/en/14/index.html)
4. [Brief alembic demonstration](https://www.educative.io/answers/how-to-use-postgresql-database-in-fastapi)
5. [Install and configure PostgreSQL](https://ubuntu.com/server/docs/databases-postgresql)
