#! /bin/sh

set -e

aws apigateway import-rest-api \
    --endpointConfigurationTypes 'EDGE' \
    --fail-on-warnings \
    --body $1