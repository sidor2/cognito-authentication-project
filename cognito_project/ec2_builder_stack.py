from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as _ec2,
    aws_cognito as _cognito,
    aws_certificatemanager as _cm,
    # aws_sqs as sqs,
    CfnOutput,
    Fn,
    aws_route53 as _r53,
    aws_route53_targets as targets,
    aws_s3 as _s3,
    aws_cloudfront as _cloudfront,
    aws_cloudfront_origins as origins
)
from constructs import Construct



#TODO Automate the application code deployment to the S3 bucket
#TODO Figure out what the first bucket is for
#TODO Check if destination bucket for www.domain.com exists, if not, create
#TODO Define the creation and deletion order

class Ec2BuilderStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        userPoolId=Fn.import_value('userPoolId')
        userPoolWebClientId=Fn.import_value('userPoolWebClientId')
        authdomain=Fn.import_value('AuthDomain')
        redirectSignIn=Fn.import_value('redirectSignIn')
        redirectSignOut=Fn.import_value('redirectSignOut')
        destinationS3=Fn.import_value('DestinationS3')

        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.MINIMAL,
            
        )
