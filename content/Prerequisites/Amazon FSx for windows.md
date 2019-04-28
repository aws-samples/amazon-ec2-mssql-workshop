+++
title = "Amazon FSx for windows"
date = 2019-03-21T20:40:20+02:00
weight = 3
chapter = false
pre = "<b>3. </b>"
+++

[Amazon FSx for Windows File Server](https://aws.amazon.com/fsx/windows/) provides a fully managed native Microsoft Windows file system so you can easily move your Windows-based applications that require file storage to AWS. Built on Windows Server, Amazon FSx provides shared file storage with the compatibility and features that your Windows-based applications rely on, including full support for the SMB protocol and Windows NTFS, Active Directory (AD) integration, and Distributed File System (DFS). Amazon FSx uses SSD storage to provide the fast performance your Windows applications and users expect, with high levels of throughput and IOPS, and consistent sub-millisecond latencies. This compatibility and performance is particularly important when moving workloads that require Windows shared file storage, like CRM, ERP, and .NET applications, as well as home directories.

With Amazon FSx, you can launch highly durable and available Windows file systems that can be accessed from up to thousands of compute instances using the industry-standard SMB protocol. Amazon FSx eliminates the typical administrative overhead of managing Windows file servers. You pay for only the resources used, with no upfront costs, minimum commitments, or additional fees.

## Deploy FSx

1. Go to FSx service in Ireland [link](https://eu-west-1.console.aws.amazon.com/fsx/home?region=eu-west-1#landing) and click on "Create file system"

1. Select Amazon FSx for Windows File Server

1. Create new File system with 500-GB Storage in **eu-west-1c** , in the Directory, choose the directory from Step 1.2. *If not listed, the directory is not ready for use* 

![setup-directory](/img/Steps/FSx-details.png?classes=border,shadow)

1. Monitor the progress of the FSx

![setup-directory](/img/Steps/FSx-review.png?classes=border,shadow)

1. Add the VPC CIDR to FSx security group (Via the FSx console page, click on Security groups, and add the VPC cidr as Inbound rule)


{{% notice note %}}
This can take up to 10-20 Minutes. 
{{% /notice %}}

{{% notice warning %}}
FSx minimum size is 300GB, So if you only uses FSx for file share witness consider using t3 machine since FSx cost would be higher than a t3 machine running and hosting the file share for witness.
{{% /notice %}}