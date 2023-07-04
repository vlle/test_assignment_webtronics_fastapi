## Robot Youtube

## Description

This is a simple CRUD-like web API based on FastAPI, SQLALchemy and PostgreSQL.

## Features
- Basic CRUD for videos
- Availability to set like and dislike
- JWT-based authentication
- Swagger documentation available at https://127.0.0.1/docs (after running the app)
<img width="600" alt="pydocs" src="https://github.com/vlle/technical_assignemnt_webtronic_fastapi/assets/91570054/62434380-b3d2-4118-9af0-570c48b345cd">

- Pytest tests.
- <img width="600" alt="Снимок экрана 2023-07-04 в 15 38 21" src="https://github.com/vlle/technical_assignemnt_webtronic_fastapi/assets/91570054/8841dd2e-670b-40d2-82c4-c50bc9781c43">
- Redis for caching
- Attempt at creating Github Workflow for auto-testing (starts, but not finishing)


## What would I do with more time:
1) Mock more in testing - my code heavily dependents on database, so I would mock it more. And testing some of endpoints dependents on another endpoints, so I would mock it more.
2) Add more features - views, comments, etc. I also would like to add URLs to my Robot Youtube application.
3) Complete bonus tasks more!

## Usage

### Prerequisites
- Installed docker and docker-compose

### Run the app

```bash
git clone
docker-compose up
```

### Test the app

```bash
git clone
docker compose -f docker-compose.test.yml up --build
```


## Demonstration
Video: [![asciicast](https://asciinema.org/a/8tLgrkS43j7n32h3KcJMtIdEy.svg)](https://asciinema.org/a/8tLgrkS43j7n32h3KcJMtIdEy)

Examples of [httpie](https://httpie.io)  requests:
```bash
http GET "http://127.0.0.1:8000/view_post/1"
http PUT "http://127.0.0.1:8000/edit_post/1" name=new_name description=example_descr --auth-type bearer --auth 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJs
b2dpbiI6InZsbGU1In0.v41_hhdtOzJA8Y-xCwZ8q_MvVJqmdDXGto2UtfVZCo8'
http POST "http://127.0.0.1:8000/create_post" name=example_video description=example_descr --auth-type bearer --auth eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo
xLCJsb2dpbiI6InZsbGU1In0.v41_hhdtOzJA8Y-xCwZ8q_MvVJqmdDXGto2UtfVZCo8
http GET "http://127.0.0.1:8000/login?login=vlle5&password=example"
http POST "http://127.0.0.1:8000/signup" login=vlle5 password=example email=vlle5@vlle.com
```


## Tech stack
- FastAPI, SQLAlchemy, PostgreSQL, jose(jwt authentication), Docker, Pytest, pre-commit, black, isort
