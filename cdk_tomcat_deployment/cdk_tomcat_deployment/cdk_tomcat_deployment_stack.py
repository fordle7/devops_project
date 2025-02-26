import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_iam as iam
import yaml
from aws_cdk import CfnOutput, CfnTag, Duration, Stack
from constructs import Construct
from network_stack import NetworkStack


class CdkTomcatDeploymentStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        network_stack: NetworkStack,
        env_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Load environment-specific configurations
        with open("parameters.yaml", "r") as f:
            config = yaml.safe_load(f).get(env_name, {})

        instance_type = config.get("instance_type", "t3.micro")
        min_capacity = config.get("min_capacity", 1)
        max_capacity = config.get("max_capacity", 3)
        desired_capacity = config.get("desired_capacity", 1)

        # Create Key Pair
        cfn_key_pair = ec2.CfnKeyPair(
            self,
            "InstanceCfnKeyPair",
            key_name="cdk-ec2-key-pair",
            tags=[CfnTag(key="key", value="value")],
        )

        # IAM Role for EC2
        role = iam.Role(
            self,
            "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                )
            ],
        )

        # Launch Instance Template
        tomcat_instance_type = ec2.InstanceType(instance_type)
        tomcat_machine_image = ec2.AmazonLinuxImage()  # select AWS linux

        launch_template = ec2.LaunchTemplate(
            self,
            "LaunchTemplate",
            instance_type=tomcat_instance_type,
            machine_image=tomcat_machine_image,
            role=role,
            security_group=network_stack.security_group,
            key_name=cfn_key_pair.key_name,  # Replace with actual key pair
        )

        # Create Auto Scaling Group
        asg = autoscaling.AutoScalingGroup(
            self,
            "ASG",
            vpc=network_stack.vpc,
            launch_template=launch_template,
            min_capacity=min_capacity,  # Minimum number of instances
            max_capacity=max_capacity,  # Maximum number of instances
            desired_capacity=desired_capacity,  # Desired number of instances at start
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),  # Choose public/private subnet
        )

        # Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=network_stack.vpc,
            internet_facing=True,  # Set to False for internal ELB
        )

        listener = alb.add_listener(
            "ALBListener",
            port=80,
            open=True,  # Allows public access
        )
        listener.add_targets(
            "ASGTargetGroup",
            port=8080,
            targets=[asg],
            health_check=elbv2.HealthCheck(
                path="/",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
            ),
        )

        # Allow incoming HTTP traffic to the ALB
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Allow public HTTP")

        # Output the ALB DNS Name
        CfnOutput(self, "ALBDNS", value=alb.load_balancer_dns_name)
