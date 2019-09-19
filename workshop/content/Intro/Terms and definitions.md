+++
title = "Terms and definitions"
weight = 11
chapter = false
pre = "<b>1. </b>"
+++

- Always on availability groups: The Always On availability groups feature is a high-availability and disaster-recovery solution that provides an enterprise-grade alternative to database mirroring. Introduced in SQL Server 2012 (11.x), Always On availability groups maximizes the availability of a set of user databases for an enterprise. An availability group supports a failover environment for a discrete set of user databases, known as availability databases, that fail over together. An availability group supports a set of read-write primary databases and one to eight sets of corresponding secondary databases. Optionally, secondary databases can be made available for read-only access and/or some backup operations.

- Availability group - A container for a set of databases, availability databases, that fail over together
- Primary replica - The availability replica that makes the primary databases available for read-write connections from clients and, also, sends transaction log records for each primary database to every replica
- Secondary replica - An availability replica that maintains a secondary copy of each availability database, and serves as a potential failover targets for the availability group. Optionally, a secondary replica can support read-only access to secondary databases can support creating backups on secondary databases
- Availability group listener - **A server name** to which clients can connect in order to access a database in a primary or secondary replica of an Always On availability group. Availability group listeners direct incoming connections to the primary replica or to a read-only secondary replica

In this workshop, you are going to build basic high availability cluster

{{% notice info %}}
**SQL Standard:** Provides basic high availability: two-node single database failover, non-readable secondary **vs.**
**SQL Enterprise:** with advanced high availability: Always On Availability Groups, multi-database failover, readable secondaries
{{% /notice %}}