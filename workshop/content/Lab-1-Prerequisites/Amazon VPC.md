+++
title = "Amazon VPC"
date = 2019-03-21T20:40:20+02:00
weight = 11
chapter = false
pre = "<b>1. </b>"
+++

Amazon Virtual Private Cloud (Amazon VPC) lets you provision a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define. You have complete control over your virtual networking environment, including selection of your own IP address range, creation of subnets, and configuration of route tables and network gateways. You can use both IPv4 and IPv6 in your VPC for secure and easy access to resources and applications.

## VPC Details

Create a VPC with the following settings

Name: MS-SQL-POC
CIDR: 10.0.0.0 / 16

![VPC](/images/screenshots/Steps/vpc-settings.png?classes=border,shadow)

Now, create 3 Subnets:

![subnet-settings](/images/screenshots/Steps/subnet-settings.png?classes=border,shadow)

Site-1 subnet: 10.0.1.0/24 – **eu-west-1a**

Site-2 subnet: 10.0.2.0/24 – **eu-west-1b**

Site-3 subnet: 10.0.3.0/24 - **eu-west-1c**

Create Internet-Gateway, attach it to the VPC and change the main route-table.

![ig-attached](/images/screenshots/Steps/ig-attached.png?classes=border,shadow)

Make sure that the route table configured as following:

![rt-result](/images/screenshots/Steps/rt-result.png?classes=border,shadow)
