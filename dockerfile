FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt install python3-pip -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 compiler.py

RUN /bin/bash -c  "find /app/ -name '*.py' -type f -delete"
RUN /bin/bash -c "find /app/ -name "dockerfile" -type f -delete"
RUN /bin/bash -c "find /app/ -name "compiler.pyc" -type f -delete"

CMD python3 script.pyc /app/Images /app/Results monkey
