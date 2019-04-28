+++
title = "AWS Directory service"
date = 2019-03-21T20:40:20+02:00
weight = 2
chapter = false
pre = "<b>2. </b>"
+++

[AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_microsoft_ad.html) lets you run Microsoft Active Directory (AD) as a managed service. AWS Directory Service for Microsoft Active Directory, also referred to as AWS Managed Microsoft AD, is powered by Windows Server 2012 R2. When you select and launch this directory type, it is created as a highly available pair of domain controllers connected to your virtual private cloud (VPC). The domain controllers run in different Availability Zones in a region of your choice. Host monitoring and recovery, data replication, snapshots, and software updates are automatically configured and managed for you.

With AWS Managed Microsoft AD, you can run directory-aware workloads in the AWS Cloud, including Microsoft SharePoint and custom .NET and SQL Server-based applications. You can also configure a trust relationship between AWS Managed Microsoft AD in the AWS Cloud and your existing on-premises Microsoft Active Directory, providing users and groups with access to resources in either domain, using single sign-on (SSO).

## Create Managed AD for the domain authentication

In this task, you will create a Managed Directory.

Navigate to Directory Service and click &quot;Set up directory&quot;
![create-new-mad](/img/Steps/create-new-mad.png?classes=border,shadow)

Type: Choose &quot;AWS Managed Microsoft AD&quot;
And fill the details as following:
**Change the directory name to your name**
**Set strong password, but write it down, you will need this password**

![setup-directory](/img/Steps/mad-settings.png?classes=border,shadow)

For the VPC and Subnet, please use the VPC provided in your account (or that you created)
![setup-directory](/img/Steps/mad-vpc.png?classes=border,shadow)

Review:
![setup-directory](/img/Steps/mad-review.png?classes=border,shadow)

Add the VPC CIDR to DS security group (Via the DS console page, click on Security groups, and add the VPC cidr as Inbound rule)

{{% notice note %}}
**This can take up to 20-45 minutes.**
{{% /notice %}}

