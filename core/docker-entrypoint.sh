#!/bin/sh

set -e

./wait-for-it.sh rabbitmq:5672 -- echo "rabbitmq is up"

exec "$@"
#echo "$1"
