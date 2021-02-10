+++
title = "Prerequisites (Infrastructure)"
date = 2019-09-19T12:42:59-07:00
weight = 20
chapter = false
pre = "<b>Lab-1: </b>"
+++


In this section you will learn how to launch Amazon FSx to be part of AWS Directory Service AD domain, configure your workstation to remotely send commands to the servers using CloudFormation or AWS Console.

**It's recommended not to use the CloudFormation script, you will learn more from doing and configure everything by yourself.**

{{% notice tip %}}
If you are using an account from the AWS EventEngine, it will already have the CloudFormation deployed.
It's still recommended to review the steps, but you don't need to launch the CloudFormation template again or create the resources manually.
Continue to **[Step 1.4](/lab-1-prerequisites/automations-management.html#aws-tools-for-powershell)**
{{% /notice %}}

### Automated

Use the following CloudFormation Template

The CloudFormation template contains:

- VPC with 3 Subnets
- Security Group
- IAM Role for EC2 (Instance Role)
- AWS Managed Microsoft AD
- Amazon FSx (500GB Storage) connected to the AWS Managed Microsoft AD

CloudFormation Link:
https://github.com/aws-samples/amazon-ec2-mssql-workshop/blob/master/resources/templates/mssql-stack-root.yaml

### Manually

{{% children showhidden="false" %}}


Please note:
As this is for a lab exercise we only use 3 public-subnets but it's not recommend in a production environment. In a production environment we will deploy a private subnet as well.
