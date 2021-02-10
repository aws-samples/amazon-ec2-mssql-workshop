+++
title = "Architecture"
weight = 12
chapter = false
pre = "<b>2. </b>"
+++


## Architecture

You are going to build the following architecture:

![Architecture](/images/screenshots/Architecture/mssql-draw-workshop-Page-1.png?classes=border,shadow)

### Architecture components:

+ [Amazon VPC](https://aws.amazon.com/vpc/) Provision a logically isolated section of the Amazon Web Services (AWS) Cloud where you can launch AWS resources in a virtual network that you define.

+ [AWS Directory service](https://aws.amazon.com/directoryservice/) also known as AWS Managed Microsoft AD is built on actual Microsoft Active Directory and does not require you to synchronize or replicate data from your existing Active Directory to the cloud. With AWS Managed Microsoft AD, you will easily join the Amazon EC2 instances to the an AD domain, to build the SQL Fail-Over cluster.

+ [Amazon FSx for Windows File Server](https://aws.amazon.com/fsx/windows/) is a fully managed native Microsoft Windows file system. Amazon FSx provides shared file storage with the compatibility and features that your Windows-based applications rely on, including full support for the SMB protocol and Windows NTFS, Active Directory (AD) integration. **In this workshop, we will use Amazon FSx for a SQL Witness server and as a FileShare location**

+ [NVMe SSD Instance Store Volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html) - An instance store provides temporary block-level storage for your instance. This storage is located on disks that are physically attached to the host computer. Instance store is ideal for temporary storage of information that changes frequently, such as buffers, caches, scratch data, and other temporary content, or for data that is replicated across a fleet of instances, such as a load-balanced pool of web servers.

    Instance with NVMe drive: ([Full list](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html))

    - Amazon EC2 i3 and i3en
    - Amazon EC2 c5d and c5ad
    - Amazon EC2 f1
    - Amazon EC2 m5d, m5ad and m5dn
    - Amazon EC2 r5d, r5ad, r5dn
    - Amazon EC2 x1 and x1e
    - Amazon EC2 z1d
    - Amazon EC2 i3en

    These instances include Non-Volatile Memory Express (NVMe) SSD-based instance storage optimized for low latency, very high random I/O performance, and high sequential read throughput, and deliver high IOPS at a low cost.

    **In this workshop, we will use the c5ad.xlarge EC2 instance type, and the NVMe drive for hosting the TempDB**

+ [AWS Systems Manager](https://aws.amazon.com/systems-manager/) - AWS Systems Manager gives you visibility and control of your infrastructure on AWS. Systems Manager provides a unified user interface so you can view operational data from multiple AWS services and allows you to automate operational tasks across your AWS resources. With Systems Manager, you can group resources, like Amazon EC2 instances, Amazon S3 buckets, or Amazon RDS instances, by application, view operational data for monitoring and troubleshooting, and take action on your groups of resources. Systems Manager simplifies resource and application management, shortens the time to detect and resolve operational problems, and makes it easy to operate and manage your infrastructure securely at scale.


Let's start building!
