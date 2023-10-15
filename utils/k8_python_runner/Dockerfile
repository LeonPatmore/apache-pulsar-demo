FROM python:3.11-alpine

RUN pip install pipenv

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "entry/main.py"]
