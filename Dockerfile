FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN pip install pytest

ENV PYTHONPATH=.

RUN pytest --version

CMD [ "pytest" ]