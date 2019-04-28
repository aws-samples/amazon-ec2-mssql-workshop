+++
title = "Server configurations"
date = 2019-03-21T20:40:20+02:00
weight = 2
chapter = false
pre = "<b>2. </b>"
+++

## Prepare SQL Server and Pacemaker cluster ##

- Use AWS Systems Manager Session Manager to change SQL Server SA password, using this command:

```bash
#Do these on both instances
sudo /opt/mssql/bin/mssql-conf set-sa-password
sudo systemctl start mssql-server
sudo /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YOUR_SA_PASSWORD -i /opt/mssql/move_tempdb.sql
sudo passwd hacluster

sudo /opt/mssql/configure_ha.sh

#Do this on instance 1 only:
sudo /opt/mssql/create_pcm_cluster.sh
```

## Create certificates and endpoints ##

- Use AWS Systems Manager Session Manager and SQL Server Linux client tool to create AG endpoints and certificates. You have to create a certificate on each node and copy it across to the other node

```SQL
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<StrongPassword>';

GO

CREATE CERTIFICATE AGNLE1_Cert
WITH SUBJECT = 'AGNLE1 AG Certificate';

GO

BACKUP CERTIFICATE AGNLE1_Cert
TO FILE = '/var/opt/mssql/data/AGNLE1_Cert.cer';

GO

CREATE ENDPOINT AGEP
STATE = STARTED
AS TCP (
    LISTENER_PORT = 5022,
    LISTENER_IP = ALL)
FOR DATABASE_MIRRORING (
    AUTHENTICATION = CERTIFICATE AGNLE1_Cert,
    ROLE = ALL);

GO
```

- Repeat above for node 2:

```SQL
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<StrongPassword>';

GO

CREATE CERTIFICATE AGNLE2_Cert
WITH SUBJECT = 'AGNLE2 AG Certificate';

GO

BACKUP CERTIFICATE AGNLE2_Cert
TO FILE = '/var/opt/mssql/data/AGNLE2_Cert.cer';

GO

CREATE ENDPOINT AGEP
STATE = STARTED
AS TCP (
    LISTENER_PORT = 5022,
    LISTENER_IP = ALL)
FOR DATABASE_MIRRORING (
    AUTHENTICATION = CERTIFICATE AGNLE2_Cert,
    ROLE = ALL);

GO
```

- Now copy certificates from each node to the other. First use your SSM Session Manager session on node 1:

```bash
#Use S3 to Copy the certificate between nodes
#Instance 1: 
sudo aws s3 cp /var/opt/mssql/data/AGNLE1_Cert.cer s3://ss-experiments/AGNLE1_Cert.cer
```

- Now use your SSM Session Manager session on node 2:

```bash
#Use S3 to Copy the certificate between nodes
#Instance 2: 
sudo aws s3 cp /var/opt/mssql/data/AGNLE2_Cert.cer s3://ss-experiments/AGNLE2_Cert.cer
sudo aws s3 cp s3://ss-experiments/AGNLE1_Cert.cer /var/opt/mssql/data/AGNLE1_Cert.cer
sudo chown mssql:mssql /var/opt/mssql/data/AGNLE1_Cert.cer

sudo /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YOUR_SA_PASSWORD
CREATE LOGIN AGNLE1_Login WITH PASSWORD = '<StrongPassword>';
CREATE USER AGNLE1_User FOR LOGIN AGNLE1_Login;
GO
CREATE CERTIFICATE AGNLE1_Cert
AUTHORIZATION AGNLE1_User
FROM FILE = '/var/opt/mssql/data/AGNLE1_Cert.cer';
GO
GRANT CONNECT ON ENDPOINT::AGEP TO AGNLE1_Login;
GO
```

- Go back to SSM Session Manager session on node 1 and finish this step:

```bash
#Use S3 to Copy the certificate between nodes
#Instance 1: 
sudo aws s3 cp s3://ss-experiments/AGNLE2_Cert.cer /var/opt/mssql/data/AGNLE2_Cert.cer
sudo chown mssql:mssql /var/opt/mssql/data/AGNLE2_Cert.cer

sudo /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P YOUR_SA_PASSWORD
CREATE LOGIN AGNLE2_Login WITH PASSWORD = '<StrongPassword>';
CREATE USER AGNLE2_User FOR LOGIN AGNLE2_Login;
GO
CREATE CERTIFICATE AGNLE2_Cert
AUTHORIZATION AGNLE2_User
FROM FILE = '/var/opt/mssql/data/AGNLE2_Cert.cer';
GO
GRANT CONNECT ON ENDPOINT::AGEP TO AGNLE2_Login;
GO
```