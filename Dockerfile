FROM ubuntu:latest

COPY /raja /opt/src/raja
COPY requirements.txt /opt/src/requirements.txt
COPY setup.py /opt/src/setup.py

WORKDIR /opt/src
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m", "raja"]