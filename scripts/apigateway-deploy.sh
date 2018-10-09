#! /bin/sh

set -e

aws apigateway import-rest-api --fail-on-warnings --body file://$1