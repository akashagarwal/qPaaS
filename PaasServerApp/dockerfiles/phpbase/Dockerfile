############################################################
# Dockerfile to build PHP Application Containers
# Based on Ubuntu latest version
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER team2

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install php and basic php tools
RUN apt-get install -y apache2 libapache2-mod-php5 php5-mysql php5-gd php5-curl php-pear php-apc

# Update pear
#RUN pear config-set http_proxy $http_proxy
RUN pear update-channels
