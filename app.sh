#!/usr/bin/env bash
FUNCTION=
if [ ! -z $1 ]; then
    FUNCTION="$1"
fi

platform='unknown'
unmaster=`uname`

if [[ $unmaster == 'Linux' ]]; then
   platform='linux'
elif [[ $unmaster == 'MINGW64_NT-10.0' ]]; then
    platform='windows'
elif [[ $unmaster == 'Darwin' ]]; then
   platform='mac'
fi




show-help() {
    echo 'Functions:'
    echo './app.sh [start] [stop] [restart] [build] [first_run]'
}

rundocker() {
    echo 'Stop all containert'
    docker stop $(docker ps -a -q)
    echo ''
    echo 'Start containers'
    docker-compose -p rd-cmg-consul-backend up -d 
    echo ''
}

start() {
    rundocker
    migrate
    #create_static
}

migrate() {
    docker exec -it rd-cmg-consul-backend_web_1 python manage.py migrate

}

createsuperuser() {
    docker exec -it rd-cmg-consul-backend_web_1 python manage.py createsuperuser

}


makemigrations() {
    docker exec -it rd-cmg-consul-backend_web_1 python manage.py makemigrations

}


collectstatic() {
    docker exec -it rd-cmg-consul-backend_web_1 bash -c "cd app && npm i && npm run build"
    docker exec -it rd-cmg-consul-backend_web_1 python manage.py collectstatic
}





stop() {
    echo 'Stop all containert'
    docker stop $(docker ps -a -q)
}

restart() {
    start
}

first_run() {
    local DB_NAME=$(get_variable 'DB_NAME')
    local DB_USER=$(get_variable 'DB_USER')
    local DB_PASS=$(get_variable 'DB_PASS')
    rundocker
    docker exec -it rd-cmg-consul-backend_postgres_1 psql -U postgres -c "CREATE DATABASE $DB_NAME;"
    docker exec -it rd-cmg-consul-backend_postgres_1 psql -U postgres -c  "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASS';"
    docker exec -it rd-cmg-consul-backend_postgres_1 psql -U postgres -c  "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO  $DB_USER;"
    start
}

update() {
   echo 'Build containers with cache'
   docker-compose -p rd-cmg-consul-backend build web 
}




build() {
   echo 'Build containers'
   docker-compose -p rd-cmg-consul-backend build --no-cache 
}


get_variable(){
    while read p; do
      A="$(echo $p | cut -d'=' -f1)"
      B="$(echo $p | cut -d'=' -f2)"
      if [[ $A = $1 ]]
      then
        echo $B
      fi
    done <.env
}

case "$1" in
-h|--help)
    show-help
    ;;
*)
    if [ ! -z $(type -t $FUNCTION | grep function) ]; then
        $1
    else
        show-help
    fi
esac