+++
title = "Welcome to MS-SQL Availability Group Workshop"
date = 2019-03-24T20:40:20+02:00
weight = 1
pre = "<b>X. </b>"
+++

## Welcome to MS-SQL Availability Group Workshop

The Always On availability groups feature is a high-availability and disaster-recovery solution that provides an enterprise-grade alternative to database mirroring. Introduced in SQL Server 2012 (11.x), Always On availability groups maximizes the availability of a set of user databases for an enterprise. An availability group supports a failover environment for a discrete set of user databases, known as availability databases, that fail over together. An availability group supports a set of read-write primary databases and one to eight sets of corresponding secondary databases. Optionally, secondary databases can be made available for read-only access and/or some backup operations.

{{% notice info %}}
**SQL Standard:** Provides basic high availability: two-node single database failover, non-readable secondary **vs.**
**SQL Enterprise:** with advanced high availability: Always On Availability Groups, multi-database failover, readable secondaries
{{% /notice %}}

In this workshop, you are going to build basic high availability.
 
## Architecture

You are going to build the following architecture:

![Architecture](/img/Architecture/mssql-draw-workshop-Page-1.png?classes=border,shadow)

### Architecture components:

+ [Amazon VPC](https://aws.amazon.com/vpc/) Provision a logically isolated section of the Amazon Web Services (AWS) Cloud where you can launch AWS resources in a virtual network that you define.

+ [AWS Directory service](https://aws.amazon.com/directoryservice/) also known as AWS Managed Microsoft AD is built on actual Microsoft Active Directory and does not require you to synchronize or replicate data from your existing Active Directory to the cloud. With AWS Managed Microsoft AD, you will easily join the Amazon EC2 instances, and build the Fail-over cluster.

+ [Amazon FSx for Windows File Server](https://aws.amazon.com/fsx/windows/) is a fully managed native Microsoft Windows file system. Amazon FSx provides shared file storage with the compatibility and features that your Windows-based applications rely on, including full support for the SMB protocol and Windows NTFS, Active Directory (AD) integration. **In this workshop, we will use FSx for Witness server, and FileShare location**

+ [NVMe SSD Instance Store Volumes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html) - An instance store provides temporary block-level storage for your instance. This storage is located on disks that are physically attached to the host computer. Instance store is ideal for temporary storage of information that changes frequently, such as buffers, caches, scratch data, and other temporary content, or for data that is replicated across a fleet of instances, such as a load-balanced pool of web servers.

    Instance with NVMe drive: ([Full list](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html))

    - Amazon EC2 i3
    - Amazon EC2 c5d
    - Amazon EC2 f1
    - Amazon EC2 m5d and m5ad
    - Amazon EC2 r5d and r5ad
    - Amazon EC2 z1d
    - Amazon EC2 i3en
    
    These instances include Non-Volatile Memory Express (NVMe) SSD-based instance storage optimized for low latency, very high random I/O performance, and high sequential read throughput, and deliver high IOPS at a low cost. 
    
    **In this workshop, we will use r5d.xlarge instance type, and the NVMe drive for host the TempDB**

+ [AWS Systems Manager](https://aws.amazon.com/systems-manager/) - AWS Systems Manager gives you visibility and control of your infrastructure on AWS. Systems Manager provides a unified user interface so you can view operational data from multiple AWS services and allows you to automate operational tasks across your AWS resources. With Systems Manager, you can group resources, like Amazon EC2 instances, Amazon S3 buckets, or Amazon RDS instances, by application, view operational data for monitoring and troubleshooting, and take action on your groups of resources. Systems Manager simplifies resource and application management, shortens the time to detect and resolve operational problems, and makes it easy to operate and manage your infrastructure securely at scale.

## Main goals

- Get familiar with AWS Directory Service and Amazon FSX for Windows
- Understand how to automate and remotely manage windows server
- Build well-architected self-managed MS-SQL on AWS
- Explore ways to use AWS System Manager to run scripts on servers
- Understand the value of Local NVMe drives and how to use it to get more performance
- Understand the value of striping gp2 and how to automate the process
- Build full solution of Always On availability group 


## Terms and Definitions

- Availability group - A container for a set of databases, availability databases, that fail over together
- Primary replica - The availability replica that makes the primary databases available for read-write connections from clients and, also, sends transaction log records for each primary database to every replica
- Secondary replica - An availability replica that maintains a secondary copy of each availability database, and serves as a potential failover targets for the availability group. Optionally, a secondary replica can support read-only access to secondary databases can support creating backups on secondary databases
- Availability group listener - **A server name** to which clients can connect in order to access a database in a primary or secondary replica of an Always On availability group. Availability group listeners direct incoming connections to the primary replica or to a read-only secondary replica