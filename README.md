
# Cognito ACG Lab solution project!
https://learn.acloud.guru/handson/86873530-816c-49bf-b81e-fea5e4fb315c


This project creates a Cognito user pool with an associated App client and a custom domain for authentication. The Cognito user pool allows users to sign up, sign in, and access their user profile. The custom domain is configured with Amazon Route 53 and AWS Certificate Manager to enable secure HTTPS communication.

## Description
<img src="./diagram.png" alt="CDK App Architecture Diagram" width="50%" height="25%">

The CognitoProjectStack creates the following resources:
### Cognito User Pool

- A Cognito User Pool named "CognitoLab" is created.
- The user pool allows self sign-up and verifies user emails automatically.
- The user pool has an associated app client named "CognitoLabApp" with OAuth settings for authorization code grant flow.
- The app client callback and logout URLs are set to https://www.<your_domain_name>.

### Custom Domain

- An Amazon Certificate Manager (ACM) certificate is created for *.<your_domain_name> to secure the custom domain communication.
- The user pool is associated with a custom domain named "auth.<your_domain_name>".

### S3 Buckets

- Two S3 buckets are used as CloudFront origins, one for the domain root and another for the "www" subdomain.

### CloudFront Distribution

- A CloudFront distribution is created with default behavior set to redirect HTTP requests to HTTPS.
- The distribution uses the previously created ACM certificate for secure communication.
- The default behavior points to the "www" subdomain S3 bucket.

### Amazon Route 53 Records

- An A record is created for the root domain (<your_domain_name>) to point to the CloudFront distribution.
- A CNAME record is created for the "www" subdomain to point to the CloudFront distribution.

### Outputs

After a successful deployment, the following outputs will be shown:

- userPoolId: The ID of the Cognito user pool.
- userPoolWebClientId: The ID of the Cognito app client.
- AuthDomain: The custom domain name for Cognito authentication.
- RedirectSignIn: The URL to redirect users after signing in.
- RedirectSignOut: The URL to redirect users after signing out.
- DestinationS3: The name of the S3 bucket used as the CloudFront origin for the "www" subdomain.
- cognitocfdomainalias: The CloudFront domain alias for the custom domain.

## Prerequisites

Before deploying this stack, ensure you have the following prerequisites:
1. An AWS account with appropriate permissions to create resources such as Cognito User Pools, S3 Buckets, CloudFront Distributions, Route 53 Records, and ACM Certificates.

## Deployment Steps

1. Ensure you have the AWS CLI configured with the appropriate credentials and region.
2. Deploy the CDK stack using the following command:

To manually create a virtualenv on MacOS and Linux:
```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.
```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:
```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```

Configure AWS access key
```
$ aws configure
```

Bootstrap the account
```
$ cdk bootstrap
```

Add the required values in the `exports.sh` file and run it
```
$ . exports.sh
```

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk ls
```

Deploy the stack. Make sure to save the outputs into `cdk-outputs.json`
```
$ cdk deploy CognitoProjectStack --require-approval=never --outputs-file ./cdk-outputs.json
```

Once the infrastructure deployment is fully complete, deploy the front end code
```
$ ./build.sh
```

Navigate to the lab domain
`cmcloudlab<id>.info`