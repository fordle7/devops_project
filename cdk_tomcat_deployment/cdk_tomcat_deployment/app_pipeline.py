# CI/CD for Java Tomcat applications.
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as cp_actions
import aws_cdk.aws_s3 as s3
from aws_cdk import SecretValue, Stack
from cdk_tomcat_deployment_stack import CdkTomcatDeploymentStack
from constructs import Construct


class AppPipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        compute_stack: CdkTomcatDeploymentStack,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        artifact_bucket = s3.Bucket(self, "ArtifactBucket")

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        # CodeBuild Project
        build_project = codebuild.PipelineProject(
            self,
            "BuildProject",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0
            ),
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {"build": {"commands": ["mvn clean package"]}},
                    "artifacts": {"files": ["target/*.war"]},
                }
            ),
        )

        # CodePipeline
        self.pipeline = codepipeline.Pipeline(
            self,
            "AppPipeline",
            artifact_bucket=artifact_bucket,
            stages=[
                {
                    "stageName": "Source",
                    "actions": [
                        cp_actions.GitHubSourceAction(
                            action_name="GitHub",
                            output=source_output,
                            oauth_token=SecretValue.secrets_manager("github-token"),
                            owner="your-github-user",
                            repo="your-repo",
                            branch="main",
                        )
                    ],
                },
                {
                    "stageName": "Build",
                    "actions": [
                        cp_actions.CodeBuildAction(
                            action_name="Build",
                            project=build_project,
                            input=source_output,
                            outputs=[build_output],
                        )
                    ],
                },
                {
                    "stageName": "Deploy",
                    "actions": [
                        cp_actions.S3DeployAction(
                            action_name="Deploy",
                            bucket=artifact_bucket,
                            input=build_output,
                        )
                    ],
                },
            ],
        )
