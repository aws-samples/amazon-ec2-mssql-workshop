## Amazon EC2 MSSQL Workshop

Workshop for building a MS-SQL Always On Basic Availability Group on Windows and Linux server in AWS

The website for this workshops is available at https://www.ec2mssqlworkshop.com/


## Summary of the workshop

In this workshop you will use Amazon FSx for Windows File Server (Managed), AWS Directory services for Identity Management and Amazon EC2 to create a Well-Architected Microsoft SQL Server solution.
The workshop also includes ways to achieve better performance from the storage layer, ways to automate this process and cover options to refactor and modernize your Microsoft database with Amazon DMS and Amazon SCT to another MySQL engine or Linux host server.

![image](https://github.com/aws-samples/amazon-ec2-mssql-workshop/blob/master/workshop/static/images/screenshots/Architecture/mssql-draw-workshop-Page-1.png)

## Key resources

1. Storage Space script : [amazon-ec2-mssql-workshop/resources/code/storage_layer.ps1](https://github.com/aws-samples/amazon-ec2-mssql-workshop/blob/master/resources/code/storage_layer.ps1)
2. Deck for this workshop : [deck/MSSQL Workshop.pdf](https://github.com/aws-samples/amazon-ec2-mssql-workshop/blob/master/deck/MSSQL%20Workshop.pdf)
3. CloudFormation template for creating the stack (steps 1 -> 1.4) [resources/templates/mssql-stack-root.yaml](https://github.com/aws-samples/amazon-ec2-mssql-workshop/blob/master/resources/templates/mssql-stack-root.yaml)

## Building the Workshop site

The content of the workshops is built using [hugo](https://gohugo.io/).

To build the content
 * clone this repository
 * [install hugo](https://gohugo.io/getting-started/installing/)
 * Run hugo to generate the site, and point your browser to http://localhost:1313

```bash
hugo serve -D
```


## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.
