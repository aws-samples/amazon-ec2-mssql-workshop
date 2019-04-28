+++
title = "Failover cluster"
date = 2019-03-21T20:40:20+02:00
weight = 4
chapter = false
pre = "<b>4. </b>"
+++

## Failover Cluster Manager

### Create the cluster

-Connect to the first node with RDP

Open the failover cluster manager and click on "create new cluster"

- Create Cluster and add the two nodes by their IP
![stormtroopocat](/img/image014.png?classes=border,shadow)
- Click "No. I don't require support from Microsoft.."
- Cluster name: "yourname-cluster"
- Uncheck the "Add all eligible storage to the cluster"


### Configure the cluster network

- Open the FailOver Cluster Manager and fix the network settings:
    - In the "Cluster Core Resources" Tab, select the cluster object, and click right click and properties
    ![stormtroopocat](/img/image015.png?classes=border,shadow)
    - Edit the first ip (To 10.0.1.12):
    ![stormtroopocat](/img/image016.png?classes=border,shadow)

    Result:
    ![stormtroopocat](/img/image017.png?classes=border,shadow)

You should see the status now "Online"

### Quorum Witness 

Set the FSx mount url (get it from FSx console) to set the Quorum Witness there. Since FSx is located in the third AZ, it will help the cluster decide in case of a network failure or unlikly event such an outage of AZ to set the primary node of the cluster.

- In Failover Cluster Manager, With the cluster selected, under Actions, select More Actions (in the left navigation pane), and then select Configure Cluster Quorum Settings. The "Configure Cluster Quorum Wizard" appears. Select Next.
- Select "select the quorum witness""
- Select "File share witness""
- And insert the FSx mount url


![clusteresult](/img/Steps/clusteresult.png?classes=border,shadow)

## Add the cluster object permissions to create Availability group object

In the next step, we will create the first Availability group, the Cluster object will need permissions to create new computer account for the Availability group, in order to grant those permissions do the following:

- Open dsa.msc and change the view to Advanced (View->Advanced)
- Go to the $Domainname OU -> And right click on Computers OU and select "Properties" (on the Computers OU)-> Go to the Security tab -> And **click add**
- **Find the object of the cluster ("yourname-cluster")**, and search for the following permissions:
 - "Create Computer objects"
 - "Read all properties"

![stormtroopocat](/img/image020.png?classes=border,shadow)
