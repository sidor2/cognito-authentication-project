from aws_cdk import (
    # Duration,
    Stack,
    aws_cognito as _cognito,
    aws_certificatemanager as _cm,
    # aws_sqs as sqs,
    CfnOutput,
    aws_route53 as _r53,
    aws_route53_targets as targets,
    aws_s3 as _s3,
    aws_cloudfront as _cloudfront,
    aws_cloudfront_origins as origins
)
from constructs import Construct
from aws_cdk.aws_route53 import HostedZone as _hz


#TODO Automate the application code deployment to the S3 bucket
#TODO Figure out what the first bucket is for
#TODO Check if destination bucket for www.domain.com exists, if not, create
#TODO Define the creation and deletion order

class CognitoProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, domain_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        origin_bucket=domain_name

        user_pool = _cognito.UserPool(self, "CognitoLab", 
            user_pool_name="CognitoLab",
            self_sign_up_enabled=True,
            auto_verify=_cognito.AutoVerifiedAttrs(email=True),
            sign_in_aliases=_cognito.SignInAliases(email=True),
            standard_attributes=_cognito.StandardAttributes(
                preferred_username=_cognito.StandardAttribute(
                    required=True
                ),
                email=_cognito.StandardAttribute(
                    required=True
                )
            )
        )
        
        app_client = user_pool.add_client(
            "CognitoLabApp", 
            generate_secret=False,
            o_auth=_cognito.OAuthSettings(
                flows=_cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False
                ),
                scopes=[_cognito.OAuthScope.OPENID, _cognito.OAuthScope.EMAIL, _cognito.OAuthScope.PROFILE],
                callback_urls=[f"https://www.{domain_name}"],
                logout_urls=[f"https://www.{domain_name}"]
            )
        )

        hzone = _hz.from_lookup(self, "AppHostedZone", domain_name=domain_name)

        domain_cert = _cm.Certificate(
            self, 
            "DomainCertificate", 
            domain_name=f"*.{domain_name}",
            validation=_cm.CertificateValidation.from_dns(hosted_zone=hzone)
        )


        target_website = _s3.Bucket.from_bucket_name(self, "OriginBucket",
            bucket_name=origin_bucket
        )
        
        target_website_www = _s3.Bucket.from_bucket_name(self, "OriginBucketWww",
            bucket_name=f"www.{origin_bucket}"
        )

        _r53.ARecord(self, "AliasToS3Point",
            zone=hzone,
            record_name="",
            target=_r53.RecordTarget.from_alias(targets.BucketWebsiteTarget(target_website))
        )
        
        up_domain = user_pool.add_domain("CustomDomain", 
            custom_domain=_cognito.CustomDomainOptions(
            domain_name=f"auth.{domain_name}",
            certificate=domain_cert)
        )

        up_domain.node.add_dependency(domain_cert)
        # domain_cert.node.add_dependency(up_domain)
        
        _r53.ARecord(self, "AliasToCFDomain",
            zone=hzone,
            record_name="auth",
            target=_r53.RecordTarget.from_alias(targets.UserPoolDomainTarget(up_domain))
        )
        
        cfd = _cloudfront.Distribution(self, "CognitoProject",
            default_behavior=_cloudfront.BehaviorOptions(
                origin=origins.S3Origin(target_website_www),
                viewer_protocol_policy=_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS                                    
            ),
            domain_names=[f"www.{domain_name}"],
            certificate=domain_cert,
            default_root_object="index.html"
        )

        # try it next time. did not commit yet.
        cfd.node.add_dependency(domain_cert)
        
        _r53.CnameRecord(self, "CNAMEtoCFdist",
            zone=hzone,
            record_name="www",
            domain_name=cfd.domain_name
        )
        
        CfnOutput(self, "userPoolId", value=user_pool.user_pool_id)
        CfnOutput(self, "userPoolWebClientId", value=app_client.user_pool_client_id)
        CfnOutput(self, "AuthDomain", value=f"auth.{domain_name}")
        CfnOutput(self, "RedirectSignIn", value=f"https://www.{domain_name}")
        CfnOutput(self, "RedirectSignOut", value=f"https://www.{domain_name}")
        CfnOutput(self, "DestinationS3", value=f"{target_website_www.bucket_name}")
        CfnOutput(self, "cognitocfdomainalias", value=up_domain.cloud_front_domain_name)