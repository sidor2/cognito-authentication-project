#!/bin/bash
s3bucket=$(cat cdk-outputs.json | jq '.CognitoProjectStack.DestinationS3'| tr -d \")
cd content-aws-sam/labs/Configuring-Custom-Domain-Cognito/app/
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
cd dist
aws s3 sync . s3://$s3bucket