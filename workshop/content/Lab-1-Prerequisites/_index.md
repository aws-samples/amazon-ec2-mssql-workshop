+++
title = "Prerequisites (Infrastracture)"
date = 2019-09-19T12:42:59-07:00
weight = 20
chapter = false
pre = "<b>Lab-1: </b>"
+++


In this section you will learn how to launch Amazon FSx to be part of AWS Directory Service domain, configure your workstation to remotely send commands to the servers using Cloudformation or AWS Console.

**It's recommended not to use the CloudFormation script, you will learn more from doing and configure everything by yourself.**

{{% notice tip %}}
If you are using account from EventEngine, the account already have the Cloudformation deployed, it's still recommended reviewing the steps, but you don't need to launch the cloudformation template again or create the resources manually. Continue to **[Step1.4](/lab-1-prerequisites/automations-management.html#aws-tools-for-powershell)**
{{% /notice %}}

### Automated 

Use the following CloudFormation Template

The CloudFormation template contains: 

- VPC with 3 Subnets 
- Security Group
- IAM Role for EC2 (Instance Role)
- AWS Directory Service with Microsoft AD
- Amazon FSx (500GB Storage) connected to the Directory

CloudFormation Link: 
https://github.com/aws-samples/amazon-ec2-mssql-workshop/resources/templates/mssql-stack-root.yaml

### Manually 

{{% children showhidden="false" %}}


Please note:
As this is for a lab exercise we only use 3 public-subnets but it's not recommend in a production environment. In producation enviroment we will deploy private subnet as well.
