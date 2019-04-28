+++
title = "Infrastructure"
date = 2019-03-21T20:40:20+02:00
weight = 1
chapter = false
pre = "<b>1. </b>"
+++

## PREREQUISITES

In this section you will learn how to launch Amazon FSx to be part of AWS Directory Service domain, configure your workstation to remotely send commands to the servers.

**It's recommended not to use the CloudFormation script, you will learn more from doing and configure everything by yourself.**

{{% notice tip %}}
If you are using account from EventEngine, the account already have the Cloudformation deployed, it's still recommended reviewing the steps, but you don't need to launch the cloudformation template again or create the resources manually. Continue to **[Step1.4](/prerequisites/automations-management/#aws-tools-for-powershell)**
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
https://s3.amazonaws.com/dudut/cf/Pre.yaml

{{% notice note %}}
If you chose CloudFormation Template, or you are using account from the workshop dashboard skip to **[Step1.4](/prerequisites/automations-management/#aws-tools-for-powershell)**
{{% /notice %}}

### Manually 

{{% children showhidden="false" %}}


Please note:
As this is for a lab exercise we only use 3 public-subnets but it's not recommend in a production environment. In producation enviroment we will deploy private subnet as well.
