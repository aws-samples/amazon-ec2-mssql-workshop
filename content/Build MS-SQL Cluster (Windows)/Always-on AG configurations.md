+++
title = "Always-on AG configurations"
date = 2019-03-21T20:40:20+02:00
weight = 5
chapter = false
pre = "<b>5. </b>"
+++

### Enable backup

Create a new Database called "Database" (open SSMS and click create new database) and do a full backup for this database (right click Tasks->Backup) to the FSx drive.

You don't need to do this step on the second node, since you will set this database to be part of the AG.

In other cases, it's best practice to have backup even if you have HA solution.

### Enable Always-on

1. Open SQL Server Configuration Manager and enable the Always on checkbox
![stormtroopocat](/img/image018.png?classes=border,shadow)

### Create Availability Group

Open SSMS and create the first Availability group

{{%expand "Step by step" %}}
![stormtroopocat](/img/image021.png?classes=border,shadow)

![ao-step1](/img/Steps/ao-step1.png?classes=border,shadow)

1. Add the second instance:
![stormtroopocat](/img/image022.png?classes=border,shadow)

2. In the Listener tab set both of the IP:
![stormtroopocat](/img/Steps/ao-step-replica.png?classes=border,shadow)

{{% notice note %}}
The listener name is the endpoint to which clients \ application are connecting to
{{% /notice %}}

1. For Data Sync use the FSx or Shared folder of one of the instances: 
![stormtroopocat](/img/Steps/ao-step-datarep.png?classes=border,shadow)
{{% /expand%}}

Result:

![stormtroopocat](/img/image025.png?classes=border,shadow)

Done.

### Test the HA

Open the SSMS right click and simulate failure

or Hard shutdown the active instance from Amazon EC2 Console

![test-failover](/img/Steps/test-failover.png?classes=border,shadow)

### Fine tuning

1. Open dnsmgmt.msc
Look for the endpoint record, how many records do you see? How to solve it?
{{%expand "See solution" %}}
*Solution:*

```powershell
Get-ClusterResource $NetworkName | Set-ClusterParameter RegisterAllProvidersIP 0
```

{{% /expand%}}

1. When failover, you might notice that the cluster is trying to set the wrong IP on the instance, since only one IP can run on one instance, we can set the cluster to try running those IP only on the instance that is relevant
{{%expand "See solution" %}}
In the Failover cluster management, click on roles and select the AG role, go to Advanced policies and allow only one node per his subnet

![stormtroopocat](/img/image026.png?classes=border,shadow)
{{% /expand%}}
