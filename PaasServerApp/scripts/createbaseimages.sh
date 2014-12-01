# Build Python Base image
docker build -t "ubuntu:pythonbase" ./dockerfiles/pythonbase/

# Build PHP Base image
docker build -t "ubuntu:phpbase" ./dockerfiles/phpbase/
