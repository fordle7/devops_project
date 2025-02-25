import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_tomcat_deployment.cdk_tomcat_deployment_stack import CdkTomcatDeploymentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_tomcat_deployment/cdk_tomcat_deployment_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkTomcatDeploymentStack(app, "cdk-tomcat-deployment")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
