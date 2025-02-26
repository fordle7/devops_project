from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from constructs import Construct


class EcrRepositoryStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create ECR Repository
        self.repository = ecr.Repository(
            self, "TomcatRepository", repository_name="tomcat-9-app"
        )


class TomcatDeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # If existing VPC
        vpc = ec2.Vpc.from_lookup(self, "Vpc", is_default=True)

        # Create ECS Cluster
        cluster = ecs.Cluster(self, "TomcatCluster", vpc=vpc)

        # Create ECR Repository
        repository = ecr.Repository.from_repository_name(
            self, "TomcatRepo", "tomcat-9-app"
        )

        # Define Fargate Service with ALB
        ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "TomcatService",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(repository),
                "container_port": 8080,
            },
            public_load_balancer=True,
        )
