# Use the base image to ubuntu:pythonbase
FROM ubuntu:pythonbase

# File Author / Maintainer
MAINTAINER team2


EXPOSE 80

ADD ./flask-master /app/
RUN pip install -r /app/dependencies
WORKDIR /app
CMD python run.py
