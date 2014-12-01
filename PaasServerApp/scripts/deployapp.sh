#!/bin/bash
####################################
# $app_type
# $app_name
# $userid
####################################

extract ()
{
	path="$1"
	arg="$2"
	curpath=`pwd`
	echo $1
	cd "$1"
	case "$arg" in
		*.tar.bz2)  tar xjf "$arg"      ;;
                *.tar.gz)   tar xzf "$arg"      ;;
                *.bz2)      bunzip2 "$arg"      ;;
                *.gz)       gunzip "$arg"       ;;
                *.tar)      tar xf "$arg"       ;;
                *.tbz2)     tar xjf "$arg"      ;;
                *.tgz)      tar xzf "$arg"      ;;
                *.zip)      unzip "$arg"        ;;
                *.Z)        uncompress "$arg"   ;;
                *.rar)      rar x "$arg"        ;;  # 'rar' must to be installed
                *.jar)      jar -xvf "$arg"     ;;  # 'jdk' must to be installed
                *)          echo "'$arg' cannot be extracted via extract()" ;;
        esac
	
	cd $curpath
}
#At this point user is authenticated already and a folder same as userid exists under ./webapp/uploads/$userid/$app_name

userid=$1
app_type=$2
app_name=$3
app_framework=$4

app_path=./webapp/uploads/$userid/$app_name/

thisport=`cat ./scripts/port`
echo "this: $thisport"
let "nextport = thisport + 1"
echo "next: $nextport"
echo "this: $thisport"
echo $nextport > ./scripts/port

# Resolve app type
if [ "$app_type" == "python" ];
then
	if [ "$app_framework" == "flask" ];
	then
		# copy ./dockerfiles/pythonapp/Dockerfile to ./webapp/uploads/$userid/$app_name/Dockerfile
		cp -f ./dockerfiles/pythonapp/Dockerfile "$app_path"
		#extract tar
		file=`ls "$app_path" | grep -E 'zip|tar|tar\.bz2|tar\.gz|bz2|gz|tbz2|tgz|Z|rar|jar'`
		extract "$app_path" "$file"
		# get app directory name
		mydir=`ls -l "$app_path" | awk '{ if (match($1, /[d].*/)) { print $9 }}'`
		#echo "Sex"+$mydir
		cp "$app_path"/dependencies "$app_path"/"$mydir"
		#echo "ADD ./webapp/uploads/$userid/$app_name/$mydir /app" >> ./webapp/uploads/$userid/$app_name/Dockerfile
		echo "ADD ./"$mydir" /app/" >> "$app_path"/Dockerfile
		# requiement file will depend on framework
		echo "RUN pip install -r /app/dependencies" >> "$app_path"/Dockerfile
		echo "WORKDIR /app" >> "$app_path"/Dockerfile
		echo "CMD python run.py" >> "$app_path"/Dockerfile
		docker build -t "$userid/$app_name" "$app_path"
		docker run --name "$userid-$app_name" -p $thisport:80 -d -t "$userid/$app_name"
		echo $thisport
	elif [ "$app_framework" == "django" ];
	then
		# copy ./dockerfiles/pythonapp/Dockerfile to ./webapp/uploads/$userid/$app_name/Dockerfile
		cp -f ./dockerfiles/pythonapp/Dockerfile "$app_path"
		#extract tar
		file=`ls "$app_path" | grep -E 'zip|tar|tar\.bz2|tar\.gz|bz2|gz|tbz2|tgz|Z|rar|jar'`
		extract "$app_path" "$file"
		# get app directory name
		mydir=`ls -l "$app_path" | awk '{ if (match($1, /[d].*/)) { print $9 }}'`
		#echo "RUN apt-get install -y libpq-dev" >> "$app_path"/Dockerfile
		cp "$app_path"/dependencies "$app_path"/"$mydir"
		#echo "ADD ./webapp/uploads/$userid/$app_name/$mydir /app" >> ./webapp/uploads/$userid/$app_name/Dockerfile
		echo "ADD ./"$mydir" /app" >> "$app_path"/Dockerfile
		# requiement file will depend on framework
		echo "RUN pip install -r /app/dependencies" >> "$app_path"/Dockerfile
		echo "WORKDIR /app" >> "$app_path"/Dockerfile
		#recursively search for manage.py and run manage.py runserver
		curdir=`pwd`
		cd "$app_path/$mydir"
		startupfile=`find . -type f -name manage.py`
		cd $curdir
		echo "EXPOSE 8000" >> "$app_path"/Dockerfile
		echo "CMD python $startupfile runserver 0.0.0.0:8000" >> "$app_path"/Dockerfile
		#echo "CMD python "$startupfile" startapp "$app_name"" >> "$app_path"/Dockerfile
		docker build -t "$userid/$app_name" "$app_path"
		docker run --name "$userid-$app_name" -p $thisport:8000 -d -t "$userid/$app_name"
		echo $thisport
	fi

elif [ "$app_type" == "php" ];
then
	# copy ./dockerfiles/pythonapp/Dockerfile to ./webapp/uploads/$userid/$app_name/Dockerfile
	cp -f ./dockerfiles/phpapp/Dockerfile "$app_path"
	#extract tar
	file=`ls ./webapp/uploads/$userid/$app_name/ | grep -E 'zip|tar|tar\.bz2|tar\.gz|bz2|gz|tbz2|tgz|Z|rar|jar'`
	extract "$app_path" "$file"
	# get app directory name
	mydir=`ls -l "$app_path" | awk '{ if (match($1, /[d].*/)) { print $9 }}'`
	cp "$app_path"/dependencies "$app_path"/"$mydir"
	cp ./scripts/run.sh "$app_path"/"$mydir"
	echo "RUN mkdir -p /app && rm -fr /var/www/html && ln -s /app /var/www/html" >> "$app_path"/Dockerfile
	echo "ADD ./"$mydir" /app" >> "$app_path"/Dockerfile
	while read line
	do
		echo "RUN pear install $line" >> "$app_path"/Dockerfile
	done < "$app_path"/dependencies
	echo "WORKDIR /app" >> "$app_path"/Dockerfile
	echo 'CMD [ "bash","/app/run.sh"]' >> "$app_path"/Dockerfile
	
	docker build -t "$userid/$app_name" "$app_path"
	docker run --name "$userid-$app_name" -p $thisport:80 -d -t "$userid/$app_name"
	echo $thisport
fi


