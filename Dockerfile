FROM ubuntu:16.04
MAINTAINER Gerasimov Andrey <grsanw@gmail.com>
ENV PORT 587
ENV TIMEOUT 3600
COPY . /opt/
WORKDIR /opt
RUN apt-get update && apt-get install -y python python-pip
RUN pip install -r requirements.txt
ENTRYPOINT python /opt/base_dnsbl_check.py -u $USERNAME -p $PASSWORD -s $SERVER -r $RECIPIENT -a $ADDRESS -P $PORT -t $TIMEOUT
