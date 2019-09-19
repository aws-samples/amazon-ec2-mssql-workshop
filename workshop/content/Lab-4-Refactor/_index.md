+++
title = "Refactor"
date = 2019-09-19T12:44:53-07:00
weight = 50
chapter = false
pre = "<b>Lab-4: </b>"
+++


This is an opportunity to explore other options besides SQL Server. While there are many AWS services you could choose from,we will assume Amazon Aurora running MySQL. In this case, you will need to migrate both the schema and data from SQL Server to MySQL.

## Run AWS Schema Conversion Tool

Link to [AWS SCT](https://s3.amazonaws.com/publicsctdownload/Windows/aws-schema-conversion-tool-1.0.latest.zip) tool

- Launch the AWS Schema Conversion Tool.

- From the File menu, choose New Project.

- Change the Source Database Engine to Microsoft SQL Server.

- Change the Destination Database Engine to Amazon Aurora (MySQL Compatible).

- Compare to the diagram below and click OK.

- Choose Connect to Microsoft SQL Server from the menu bar.

*Note: If you are prompted for a driver path, use C:\Program Files\AWS Schema Conversion Tool\drivers\sqljdbc42.jar.*

Generate a report :Select the database from the tree. Right click and choose Create report.

## Review the report
Notice that schema conversion is expected to be easy, but there is work to do on the stored procedures.

- Switch to the Action Items tab. Review the issues found as a team.

- On the right side, expand the issues.

## Database Migration Service (DMS)

AWS Database Migration Service (AWS DMS) is a cloud service that makes it easy to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores. You might want to use DMS rather than a backup/restore minimize the outage needed during the migration.

Migrate the sample database to RDS using DMS. 
Read the [getting started guide](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html).