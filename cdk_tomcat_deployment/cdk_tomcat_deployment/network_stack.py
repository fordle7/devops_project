import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct


class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define a VPC
        vpc = ec2.Vpc(
            self, "MyVPC", max_azs=2
        )  # Creates a VPC with public/private subnets

        # Define an EC2 Security Group
        security_group = ec2.SecurityGroup(
            self,
            "InstanceSG",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
        )

        # Allow SSH access from anywhere (Restrict in production)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access"
        )
