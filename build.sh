#!/bin/bash
s3bucket=$(cat cdk-outputs.json | jq '.CognitoProjectStack.DestinationS3'| tr -d \")
cd ./front-end/app/
npm install
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
cd dist
aws s3 sync . s3://$s3bucket