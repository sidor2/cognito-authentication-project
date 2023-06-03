#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cognito_project.cognito_project_stack import CognitoProjectStack
from cognito_project.ec2_builder_stack import Ec2BuilderStack

app = cdk.App()

cognito_project_stack = CognitoProjectStack(app, "CognitoProjectStack", domain_name="cmcloudlab543.info",
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    env=cdk.Environment(account='307162448257', region='us-east-1')
)

Ec2BuilderStack(app, "Ec2BuilderStack",
    env=cdk.Environment(account='307162448257', region='us-east-1')
).add_dependency(cognito_project_stack)

app.synth()
