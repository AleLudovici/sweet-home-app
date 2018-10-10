#! /bin/sh

set -e

read -p 'Enter the API id: ' apiID
read -p 'Do you want to deploy to a new stage? [Y/N] ' newstage
read -p 'Name of the stage: ' name

if [ $newstage == 'Y' ]
then
	read -p 'Stage description: ' stageDescription
	read -p 'Deployment description: ' deployDescription
	
	echo 'Creating a new stage...'
	
	aws apigateway create-deployment \
	--rest-api-id $apiID \
	--stage-name $name \
	--stage-description '${stageDescription}' \
	--description '${deployDescription'}
else
	read -p 'Deployment description: ' description
	
	echo 'Deploying to ${name}'
	
	aws apigateway create-deployment \
	--rest-api-id $apiID \
	--stage-name $name \
	--description '${description}'
fi
