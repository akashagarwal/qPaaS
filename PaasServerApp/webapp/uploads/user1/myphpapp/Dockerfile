# Use the base image to ubuntu:phpbase
FROM ubuntu:phpbase

# File Author / Maintainer
MAINTAINER team2

RUN mkdir -p /app && rm -fr /var/www/html && ln -s /app /var/www/html
ADD ./myphpapp /app
WORKDIR /app
CMD [ "bash","/app/run.sh"]
