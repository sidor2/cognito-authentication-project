
# Cognito ACG Lab solution project!
https://learn.acloud.guru/handson/86873530-816c-49bf-b81e-fea5e4fb315c


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