+++
title = "Storage layer"
date = 2019-03-21T20:40:20+02:00
weight = 3
chapter = false
pre = "<b>3. </b>"
+++

## General storage layer

The storage layer is:
![Storagelayer](/images/screenshots/Architecture/mssql-draw-workshop-Page-2.png?classes=border,shadow)

## Storage spaces

Storage Spaces (not to be confused with Storage Spaces Direct) has been a part of Windows Server since the days of Windows Server 2012, and provides an easy way for you to create software-defined storage using a server's local storage resources.

To manage Windows Storage Spaces, open Server Manager and click on the File and Storage Services tab, and then click on Storage Pools.

The Storage Space is already created with the bootstrap script, make sure you see the D: drive and E: drive as the local NVMe.

Note:
The Disk Management Console is Windows Server's legacy tool for Storage Management. The Disk Management Console, which you can access by entering the Diskmgmt.msc command at the Run prompt, only shows physical storage.

## AWS Hardware layer

The table in the following link show which instance types support EBS optimization, the dedicated bandwidth to Amazon EBS, the maximum number of IOPS the instance can support if you are using a 16 KB I/O size, and the typical maximum aggregate throughput that can be achieved on that connection in MiB/s with a streaming read workload and 128 KB I/O size. Choose an EBS–optimized instance that provides more dedicated Amazon EBS throughput than your application needs; otherwise, the connection between Amazon EBS and Amazon EC2 can become a performance bottleneck.

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSOptimized.html

The following link describe the performance for the EBS Volumes:

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html

{{% notice tip %}}
Burst capability: since we use volumes below 1 TB, each ebs can burst to 3K IOPS up to 30 mins a day. You can get a peak at 12K IOPS for 30 mins a day (which can be useful when you have ETL job that only runs for about 1 hour a day for example, or an olap cube transformation)
{{% /notice %}}


## Temp DB configuration

1. Connect to the instances, with admin user (of the AWS Managed AD)

1. Open SSMS , Click on new query:

```sql
USE master;
 GO
 ALTER DATABASE tempdb
 MODIFY FILE (NAME = tempdev, FILENAME = 'E:\tempdb.mdf');
 GO
 ALTER DATABASE tempdb
 MODIFY FILE (NAME = templog, FILENAME = 'E:\templog.ldf');
 ```

 This query set the database to move the Temp DB to the Local NVMe drive.

 Run the query on the second instance as well, and restart the SQL service.


{{% notice note %}}
Stopping instances with Instance Store Volumes can cause data loss if the data is not backed up or replicated. The data in an instance store persists only during the lifetime of its associated instance. If an instance reboots (intentionally or unintentionally), data in the instance store persists. However, data in the instance store is lost under the following circumstances: The underlying disk drive fails, the instance stops or the instance terminates.
{{% /notice %}}

**This storage layer is still a great candidate for temp DB as the temp DB only exists while the SQL service process is running. Data loss cannot happen in our scenario. Temp DB will be recreated by SQL in any single case, as long as you have the database file and log file (Stored in EBS) you can ALWAYS reconstruct the temp DB without dataloss, it's done automatically by SQL when the sql service restart.**
