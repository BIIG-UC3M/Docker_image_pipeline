FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get install python3.7.2 -y
RUN apt install python3-pip -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [“python3”, “script.py”]
