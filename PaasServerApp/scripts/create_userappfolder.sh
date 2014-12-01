#!/bin/bash
# On Deploy app click event : create a folder by app_name inside ./webapp/uploads/userid
userid=$1
app_name=$2
mkdir -p ./webapp/uploads/$userid/$app_name
chmod 777 ./webapp/uploads/$userid/$app_name
printf "new directory created ./webapp/uploads/$userid/$app_name \n"
