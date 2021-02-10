+++
title = "Always-on AG configurations"
date = 2019-03-21T20:40:20+02:00
weight = 5
chapter = false
pre = "<b>5. </b>"
+++

### Enable Backup

Create a new Database called "Database" (open SQL Server Management Studio (SSMS) and click create new database) and do a full backup for this database (right click Tasks -> Backup).

You don't need to do this step on the second node, since you will set this database to be part of the AG.

In other cases, it's best practice to have a backup even if you have a High Available (HA) solution.

### Enable Always On

1. Open SQL Server Configuration Manager (SSCM) and enable the **Always On** checkbox
![stormtroopocat](/images/screenshots/image018.png?classes=border,shadow)

### Create Availability Group

Open SSMS and create the first Availability Group

{{%expand "Step by step" %}}
![stormtroopocat](/images/screenshots/image021.png?classes=border,shadow)

![ao-step1](/images/screenshots/Steps/ao-step1.png?classes=border,shadow)

1. Add the second instance:
![stormtroopocat](/images/screenshots/image022.png?classes=border,shadow)

2. In the Listener tab set both of the IPs:
![stormtroopocat](/images/screenshots/Steps/ao-step-replica.png?classes=border,shadow)

{{% notice note %}}
The listener name is the endpoint to which clients \ application are connecting to
{{% /notice %}}

1. For Data Sync use the FSx or Shared folder of one of the instances:
![stormtroopocat](/images/screenshots/Steps/ao-step-datarep.png?classes=border,shadow)
{{% /expand%}}

Result:

![stormtroopocat](/images/screenshots/image025.png?classes=border,shadow)

Done.

### Test the HA

Open the SSMS right click and simulate failure

or Hard shutdown the active instance from Amazon EC2 Console

![test-failover](/images/screenshots/Steps/test-failover.png?classes=border,shadow)

### Fine tuning

1. Open/Run **dnsmgmt.msc**
Look for the endpoint record, how many records do you see? How to solve it?
{{%expand "See solution" %}}
*Solution:*

```powershell
Get-ClusterResource $NetworkName | Set-ClusterParameter RegisterAllProvidersIP 0
```

{{% /expand%}}

1. When failing over, you might notice that the cluster is trying to set the wrong IP on the instance, since only one IP can run on one instance, we can set the cluster to try running those IP only on the instance that is relevant
{{%expand "See solution" %}}
In the Failover Cluster Management, click on **roles** and select the **AG role**, go to **Advanced policies** and allow only one node per subnet

![stormtroopocat](/images/screenshots/image026.png?classes=border,shadow)
{{% /expand%}}
