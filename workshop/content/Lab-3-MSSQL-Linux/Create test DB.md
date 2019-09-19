+++
title = "Always-on AG configurations"
date = 2019-03-21T20:40:20+02:00
weight = 3
chapter = false
pre = "<b>3. </b>"
+++

## Create a test DB and Availabilit Group ##

- At this stage we can create a test DB to be included in the AG. Do this on node 1:

```SQL
USE MASTER
GO
CREATE DATABASE TestDB
GO
CREATE TABLE dbo.Employee (EmployeeID int PRIMARY KEY CLUSTERED);
GO
INSERT INTO dbo.Employee (EmployeeID) Values (1)
INSERT INTO dbo.Employee (EmployeeID) Values (2)
INSERT INTO dbo.Employee (EmployeeID) Values (3)
GO
BACKUP DATABASE TestDB TO DISK = '/var/opt/mssql/data/TestDB.bak' WITH FORMAT;
GO
```

- Now we can create an AG and add our test DB to it. Do this on node 1:

```SQL
USE MASTER
CREATE AVAILABILITY GROUP TestAG
WITH (BASIC, CLUSTER_TYPE = EXTERNAL)
FOR DATABASE TestDB
REPLICA ON N'ip-10-0-1-233' WITH (
   ENDPOINT_URL = N'TCP://10.0.1.233:5022',
   FAILOVER_MODE = EXTERNAL,
   AVAILABILITY_MODE = SYNCHRONOUS_COMMIT),
N'ip-10-0-3-82' WITH (
   ENDPOINT_URL = N'TCP://10.0.3.82:5022',
   FAILOVER_MODE = EXTERNAL,
   AVAILABILITY_MODE = SYNCHRONOUS_COMMIT);
GO
```

- To join the second node to the AG and initiate seeding, run the following on the second node (like before, use AWS SSM Session Manager):

```SQL
ALTER AVAILABILITY GROUP TestAG JOIN WITH (CLUSTER_TYPE = EXTERNAL);

GO

ALTER AVAILABILITY GROUP TestAG GRANT CREATE ANY DATABASE;

GO
```

- SQL Server Always On Basic AG is configured. 

## Add SQL Server and AG to Pacemaker ##

- Next we have to enable Pacemaker to access SQL Server and AG. Use SSM Session Manager to run following T-SQL statements on node 1:

```SQL
CREATE LOGIN PMLogin WITH PASSWORD='<StrongPassword>';
GO
GRANT VIEW SERVER STATE TO PMLogin;
GO
GRANT ALTER, CONTROL, VIEW DEFINITION ON AVAILABILITY GROUP::<AGThatWasCreated> TO PMLogin;
GO
```

- Run these commands on both nodes:

```bash
sudo echo "PMLogin" | sudo tee /var/opt/mssql/secrets/passwd
sudo echo "<YourPassword>" | sudo tee /var/opt/mssql/secrets/passwd
sudo chmod 400 /var/opt/mssql/secrets/passwd
```

- Finally, we have to create the AG resource in Pacemaker. Run following on node 1:

```bash
sudo pcs resource create TestAG ocf:mssql:ag ag_name=TestAG meta failover-timeout=30s master notify=true
```