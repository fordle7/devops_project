# devops_project

## cdk
Create CDK and lib needed
```
npm install -g aws-cdk
mkdir cdk-tomcat-deployment/ && cd cdk-tomcat-deployment/
cdk init app --language python
```


## tomcat
- Using docker image on docker hub to set up the server.

    ```
    sudo docker pull tomcat:latest
    ```

- 

```
cdk-tomcat-deployment/
│── cdk.json
│── requirements.txt
│── app.py
│── stacks/
│   ├── network_stack.py
│   ├── compute_stack.py
│   ├── ci_cd_pipeline.py
│   ├── cdk_pipeline.py
│── config/
│   ├── parameters.yaml
└── README.md
```

- network_stack.py: Khai báo VPC, Security Groups.
- compute_stack.py: Khai báo EC2, ASG, ALB.
- ci_cd_pipeline.py: CI/CD cho ứng dụng Java Tomcat.
- cdk_pipeline.py: CDK Pipeline để triển khai hạ tầng.
- parameters.yaml: Cấu hình riêng cho từng môi trường.
