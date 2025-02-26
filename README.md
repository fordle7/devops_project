# Deploying Tomcat Application to AWS EC2 using CDK

## Prerequisites

Ensure you have the following installed on your local machine:

- [AWS CLI](https://aws.amazon.com/cli/) (configured with access credentials)
- [Node.js & npm](https://nodejs.org/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [Python](https://www.python.org/) (for CDK deployment)

## Setup AWS CDK Project

```sh
npm install -g aws-cdk
mkdir cdk-tomcat-deployment && cd cdk-tomcat-deployment
cdk init app --language python
```

## AWS Configuration

Run the following command and enter your AWS credentials:

```sh
aws configure

AWS Access Key ID [None]: YOUR_ACCESS_KEY
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: YOUR_REGION
Default output format [None]: json
```

## Project Structure

```plaintext
cdk-tomcat-deployment/
│── cdk.json
│── requirements.txt
│── app.py
│── cdk-tomcat-deployment/
│   ├── network_stack.py
│   ├── compute_stack.py
│   ├── cdk-tomcat-deployment.py
│   ├── ci_cd_pipeline.py
│   ├── cdk_pipeline.py
│   ├── cdk_stage.py
│   ├── parameters.yaml
└── README.md
```

### Description of Files

- **`network_stack.py`**: Defines VPC and Security Groups.
- **`cdk-tomcat-deployment.py`**: Defines EC2, Auto Scaling Group (ASG), and Application Load Balancer (ALB).
- **`ci_cd_pipeline.py`**: CI/CD pipeline for a Java Tomcat application.
- **`cdk_pipeline.py`**: CDK pipeline for infrastructure deployment.
- **`compute_stack.yaml`**: Build and push Docker Image to Amazon ECR.
- **`parameters.yaml`**: Environment-specific configuration.

## Deploying Infrastructure with AWS CDK

1. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   pip install cdk-nag

   ```
<!-- 2. **Bootstrap AWS CDK (if not done before)**
   ```sh
   cdk bootstrap aws://<AWS_ACCOUNT_ID>/<AWS_REGION>
   ``` -->
3. **Synthesize the CloudFormation Template**
   ```sh
   cdk synth
   ```
4. **Deploy the Stack**
   ```sh
   cdk deploy
   ```
5. **check**
    ```sh
   cdk-nag
   ```

## Deploying Tomcat Application to EC2

1. **Upload the WAR file to S3**
   ```sh
   aws s3 cp your-app.war s3://your-bucket-name/
   ```
2. **Connect to EC2 Instance**
   ```sh
   ssh -i your-key.pem ec2-user@<EC2_PUBLIC_IP>
   ```
3. **Download and Deploy Tomcat**
   ```sh
   sudo yum update -y
   sudo yum install java-11-openjdk -y
   wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz
   tar -xvzf apache-tomcat-9.0.73.tar.gz
   mv apache-tomcat-9.0.73 tomcat
   ```
4. **Move the WAR File to Tomcat Webapps Directory**
   ```sh
   mv your-app.war tomcat/webapps/
   ```
5. **Start Tomcat**
   ```sh
   ./tomcat/bin/startup.sh
   ```

## Target

app pipeline: Build docker image - > use AWS code build war file -> deploy war to EC2 for 3 envs.
-  strategy zero downtime:
    1. create at least 6 instances: 2 in dev, 2 in test, 2 in prod. (work like replicaset in k8s)
    2. trigger script to create new instance when current instance down.

cdk pipeline: build EC2 instance -> deploy to aws
- instance includes: ASG, ALB, and network/IAM needed.
- build depend on env.

monitoring idea: use cloudwatch.
- we can use this [template](./cdk_tomcat_deployment/pics/monitoring.png)