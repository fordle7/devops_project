# CDK Pipeline for infrastructure deployment.

import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as cp_actions
from aws_cdk import SecretValue, Stack
from constructs import Construct


class CDKPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_output = codepipeline.Artifact()

        self.pipeline = codepipeline.Pipeline(
            self,
            "CDKPipeline",
            stages=[
                {
                    "stageName": "Source",
                    "actions": [
                        cp_actions.GitHubSourceAction(
                            action_name="GitHub",
                            output=source_output,
                            oauth_token=SecretValue.secrets_manager("github-token"),
                            owner="your-github-user",
                            repo="your-cdk-repo",
                            branch="main",
                        )
                    ],
                },
                {
                    "stageName": "Deploy",
                    "actions": [
                        cp_actions.CodeBuildAction(
                            action_name="DeployCDK",
                            project=codebuild.PipelineProject(self, "DeployCDK"),
                            input=source_output,
                        )
                    ],
                },
            ],
        )
