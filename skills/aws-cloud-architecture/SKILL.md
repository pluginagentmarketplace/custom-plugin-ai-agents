---
name: aws-cloud-architecture
description: Design scalable AWS architectures with VPC, EC2, S3, RDS, ECS/EKS, Lambda, and high availability patterns.
---

# AWS Cloud Architecture

AWS provides a comprehensive cloud platform for building scalable, resilient applications. Master Virtual Private Clouds, compute services, storage, databases, containerization, serverless, and Infrastructure as Code for enterprise-grade deployments.

## Quick Start

**VPC with public/private subnets:**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: us-east-1a

  PrivateSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: us-east-1b
```

**ECS Fargate deployment:**

```yaml
Resources:
  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: my-app
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: '256'
      Memory: '512'
      ContainerDefinitions:
        - Name: app
          Image: myregistry.dkr.ecr.us-east-1.amazonaws.com/app:v1
          PortMappings:
            - ContainerPort: 3000
              Protocol: tcp
```

## Key Concepts

### VPC (Virtual Private Cloud)
Isolated network with subnets, route tables, and security groups:

```yaml
Resources:
  InternetGateway:
    Type: AWS::EC2::InternetGateway

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC

  PublicRoute:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway
```

### EC2 (Elastic Compute Cloud)
Virtual machines with flexible configuration:

```yaml
Resources:
  LaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateData:
        ImageId: ami-0c55b159cbfafe1f0
        InstanceType: t3.medium
        SecurityGroupIds:
          - !Ref SecurityGroup
        UserData: !Base64 |
          #!/bin/bash
          yum update -y
          yum install -y docker
          systemctl start docker
```

### S3 (Simple Storage Service)
Object storage with versioning and replication:

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-app-data
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: archive-old-versions
            NoncurrentVersionTransitions:
              - StorageClass: GLACIER
                TransitionInDays: 30
            Status: Enabled
```

### RDS (Relational Database Service)
Managed databases with automated backups:

```yaml
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: mydb
      Engine: postgres
      EngineVersion: '15.1'
      DBInstanceClass: db.t3.micro
      AllocatedStorage: 20
      MasterUsername: admin
      MasterUserPassword: !Sub '{{resolve:secretsmanager:db-password:SecretString:password}}'
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref DBSecurityGroup
      BackupRetentionPeriod: 7
      MultiAZ: true
```

### ECS/EKS
Container orchestration on AWS:

```yaml
Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: my-cluster
      ClusterSettings:
        - Name: containerInsights
          Value: enabled

  ECSService:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 3
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PrivateSubnet1
            - !Ref PrivateSubnet2
          SecurityGroups:
            - !Ref ECSSecurityGroup
```

### Lambda & API Gateway
Serverless compute with HTTP endpoints:

```yaml
Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-api-handler
      Runtime: nodejs18.x
      Handler: index.handler
      Code:
        ZipFile: |
          exports.handler = async (event) => {
            return {
              statusCode: 200,
              body: JSON.stringify({ message: 'Hello' })
            };
          };

  ApiGateway:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: my-api
      ProtocolType: HTTP
      Target: !Sub 'arn:aws:apigatewayv2:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations'
```

## Common Patterns

**High Availability with Load Balancer:**

```yaml
Resources:
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2

  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Port: 3000
      Protocol: HTTP
      VpcId: !Ref VPC
      HealthCheckPath: /health
```

**Auto Scaling Group:**

```yaml
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 3
```

**Cross-Region Replication:**

```yaml
Resources:
  ReplicationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action: sts:AssumeRole
```

## Best Practices

✅ Use VPCs and security groups to isolate resources
✅ Enable Multi-AZ for critical databases
✅ Use IAM roles instead of access keys
✅ Enable CloudTrail for audit logging
✅ Implement automated backups and disaster recovery
✅ Use Auto Scaling for high availability
✅ Enable encryption at rest and in transit
✅ Monitor with CloudWatch and set alarms
✅ Use VPC endpoints for private connectivity
✅ Tag all resources for cost allocation

## Common Pitfalls

❌ Using default VPC instead of custom VPC
❌ Storing AWS credentials in code or environment variables
❌ Not enabling versioning on S3 buckets
❌ Single Availability Zone deployments
❌ Oversized instances (use right-sizing)
❌ Not monitoring costs
❌ Leaving default security group open
❌ Not implementing backup strategies

## Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Best Practices](https://aws.amazon.com/architecture/best-practices/)
- [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
