# Use the base image to ubuntu:pythonbase
FROM ubuntu:pythonbase

# File Author / Maintainer
MAINTAINER team2


EXPOSE 80

ADD ./helloworld /app
RUN pip install -r /app/dependencies
WORKDIR /app
EXPOSE 8000
CMD python ./manage.py runserver 0.0.0.0:8000
