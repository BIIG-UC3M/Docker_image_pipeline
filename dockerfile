# syntax=docker/dockerfile:1

FROM fnndsc/ubuntu-python3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .



