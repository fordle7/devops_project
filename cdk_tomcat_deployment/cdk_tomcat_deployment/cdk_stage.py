from aws_cdk import Stage
from cdk_tomcat_deployment_stack import CdkTomcatDeploymentStack
from constructs import Construct


class CdkStage(Stage):

    def __init__(self, scope: Construct, id: str, env_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        CdkTomcatDeploymentStack(
            self, f"{env_name}-CdkTomcatDeploymentStack", env_name=env_name
        )
