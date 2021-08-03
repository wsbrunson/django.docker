#!/bin/sh

echo "Initializing postgres db..."

while ! nc -z $DATABASES_POSTGRES_HOST $DATABASES_POSTGRES_PORT; do
  sleep 1
done

echo "postgres database has initialized successfully"
fi

exec "$@"