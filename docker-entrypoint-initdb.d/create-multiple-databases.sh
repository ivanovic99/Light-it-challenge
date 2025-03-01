#!/bin/bash

set -e
set -u

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    mysql -u root -p$MYSQL_ROOT_PASSWORD <<-EOSQL
        CREATE DATABASE IF NOT EXISTS \`$database\`;
        GRANT ALL PRIVILEGES ON \`$database\`.* TO '$MYSQL_USER'@'%';
EOSQL
}

if [ -n "$MYSQL_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $MYSQL_MULTIPLE_DATABASES"
    for db in $(echo $MYSQL_MULTIPLE_DATABASES | tr ',' ' '); do
        create_database $db
    done
    echo "Multiple databases created"
fi
