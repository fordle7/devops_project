#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_tomcat_deployment.cdk_stage import CdkStage


app = cdk.App()

# Deploy to different environments
for env_name in ["dev", "test", "prod"]:
    CdkStage(app, f"{env_name}-Stage", env_name=env_name)

app.synth()
