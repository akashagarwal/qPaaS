#!/bin/bash
extract ()
{
	path="$1"
	arg="$2"
	curpath=`pwd`
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
		startupfile=`find . -type f -name run.sh`
		cd $curdir
		echo "EXPOSE 8000" >> "$app_path"/Dockerfile
		#echo "CMD python $startupfile runserver" >> "$app_path"/Dockerfile
		echo "CMD [ \"bash\",\"$startupfile\"]" >> "$app_path"/Dockerfile
		#echo "CMD python "$startupfile" startapp "$app_name"" >> "$app_path"/Dockerfile
		docker build -t "$userid/$app_name" "$app_path"
		docker run --name "$userid-$app_name" -p $thisport:8000 -d -t "$userid/$app_name"
		echo $thisport
