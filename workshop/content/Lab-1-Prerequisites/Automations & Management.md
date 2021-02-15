+++
title = "AWS Tools for PowerShell"
date = 2019-03-21T20:40:20+02:00
weight = 14
chapter = false
pre = "<b>4. </b>"
+++

In this step, you will configure your local machine to work with AWS APIs using Powershell **or** AWS CLI.

The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

The AWS Tools for PowerShell let developers and administrators manage their AWS services and resources in the PowerShell scripting environment. 


{{% notice note %}}
Please note that you can configure Powershell on Windows and macOS, and you can configure AWS CLI on Windows and macOS as well. **In this workshop, we will focus on AWS Tools for Powershell, but we will also provide alternative commands for using AWS CLI**
{{% /notice %}}


## Installing AWS Tools for Powershell

In this step, you will install AWS Tools on your local machine.

{{%expand "Windows OS" %}} 

1. Run PowerShell (with Admin shell):

```PowerShell
## Install the module
Install-Module -Name AWSPowerShell

## Import AWS PowerShell Module
import-module awspowershell

```

See screenshot for how it should look:
![powershell](/images/screenshots/Steps/aws-powershell-tools.png?classes=border,shadow)

{{% notice note %}}
If the command above isn't working, it's because you are running an old PowerShell version. In this case, you can manually download and install [AWS Tools for PowerShell](https://sdk-for-net.amazonwebservices.com/latest/AWSToolsAndSDKForNet.msi). For other troubleshooting, please see the [documentation](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html).
{{% /notice %}}

{{% /expand%}}

{{%expand "macOS" %}} 

### MacOS Users

Most of the scripts and commands that are listed in this workshop are written in Powershell, so if you're using macOS, there are few options:

- Option 1 - Install Powershell - Download and install **full PowerShell** for macOS from [Microsoft github](https://github.com/PowerShell/PowerShell), then launch the PowerShell.app from the macOS launchpad and continue with the workshop. **Using Powershell for macOS, you will be able to run commands that are listed in the windows sections (set-awscredential, etc..)**

- Option 2 - launch a windows 2019 bastion server, and continue the workshop from the bastion host. 

- Option 3 - Use AWS CLI without PowerShell 

Please note that It's not mandatory to use Powershell for macOS or Bastion host, the workshop commands can work on macOS as well via aws CLI, but their syntax will be different. 

{{% /expand%}}

### Working with Event Engine Accounts

When labs are provisioned using an AWS tool called Event Engine, you will be provided with login credentials for the event, known as a team hash code. In this section, we will walk you through how to log in.

{{% notice note %}}
The AWS account is provided free of charge for you, and you only have the permissions needed to complete the labs in this AWS account. The accounts are temporary, and we will delete them after the labs. Make sure you have read and understood the Terms & Conditions.
{{% /notice %}}

Navigate to the Event Engine login (https://dashboard.eventengine.run/dashboard) page and enter the team hash code you were provided.

Once logged in, you will be taken to the team dashboard page. 

To access the **AWS Console** for your event, click the AWS Console button, get **IAM Access Keys**, and use the "Credentials / CLI Snippets" UI.


### Configure IAM Keys on your local machine

If using the Event Engine, you can get the AccessKey, SecretKey, and SessionToken from the Event Engine dashboard for the supplied AWS IAM Role. Using your AWS Account, you can use obtain aws_access_key_id and aws_secret_access_key from the IAM Console.

The main difference between the two, the SessionToken parameter, which is only mandatory when using IAM Roles, but when using IAM Users, you only need to configure AWS Secret Key and Access key ID.

{{%expand "SSH Keys using Event Engine" %}}

Get the AccessKey, SecretKey, and SessionToken for the workshop profile.
To do so, open https://dashboard.eventengine.run/dashboard and navigate to "Credentials / CLI Snippets."

Then configure your client to work with the account with the following commands:

#### Set the keys on a windows OS using Powershell


```PowerShell

# sets the temporary session-based credentials as active in the current shell. 
Set-AWSCredential -AccessKey AKIAIOSFODNN7EXAMPLE -SecretKey wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY -SessionToken SamPleTokeN -StoreAs workshop

## See the profile
Get-AWSCredential -ListProfileDetail
```

![awscredential](/images/screenshots/Steps/awscredential.png?classes=border,shadow)


#### Set the key on a macOS or without using Powershell

- In macOS go to "~/.aws/credentials"
- In Windows go to "C:\Users\username\\.aws\credentials"
- Add the following lines:

```
[workshop]
aws_access_key_id=ASIAYZVCZ******
aws_secret_access_key=KAB5pDqdEX9qTIzGpsq******
aws_session_token=FQoGZXIvYXdzEI///////////wEaDF297q2YZD3Q0TQYtCLuAfrlKNTmvdEnn60DpUKZxphthWtjmWLDZfk1MF6FchBx0acHhMohUUYS+tzFzHYWEEpenZmeL5dAG0XVQHg83aVJxQ8C9bM8phlo5syjeLiYlkQLaOt6V3bnCVdx56aVGiD4mND2vmP6Fu46K3zOV8JRbI0Fa+FSkeVFWgVpHFuq0Mb0b7zEUU0vV35LzZQjDzBiIFrUUTKJgSh******
region=eu-west-1
```

**Change the aws_access_key_id, aws_secret_access_key, and aws_session_token from the workshop dashboard**

Each CLI command with the flag **--profile workshop** will be to that account.


{{% /expand%}}

{{%expand "SSH Keys for Personal/Work account" %}}


1. Open the IAM console at https://console.aws.amazon.com/iam/.
2. On the navigation menu, choose Users.
3. Choose your IAM user name (not the check box).
4. Open the Security credentials tab, and then choose to Create access key.
5. To see the new access key, choose Show. 

Your credentials resemble the following:

- Access key ID: AKIAIOSFODNN7EXAMPLE
- Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

{{% notice note %}}

Keep the keys confidential to protect your AWS account, and never email them. Do not share them outside your organization, even if an inquiry appears to come from AWS or Amazon.com. No one who legitimately represents Amazon will ever ask you for your secret key.
You can retrieve the secret access key only when you initially create the key pair. Like a password, you can't retrieve it later. If you lose it, you must create a new key pair.

{{% /notice %}}


#### Set the keys on a windows OS using Powershell

```PowerShell

# sets the temporary session-based credentials as active in the current shell. 
Set-AWSCredential -AccessKey AKIAIOSFODNN7EXAMPLE -SecretKey wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY -StoreAs workshop

## See the profile
Get-AWSCredential -ListProfileDetail
```

![awscredential](/images/screenshots/Steps/awscredential.png?classes=border,shadow)


#### Set the key on a macOS or without using Powershell

- In macOS go to "~/.aws/credentials" 
- In Windows go to "C:\Users\username\\.aws\credentials" 
- Add the following lines:

```
[workshop]
aws_access_key_id=ASIAYZVCZ******
aws_secret_access_key=KAB5pDqdEX9qTIzGpsq******
region=eu-west-1
```
**Change the aws_access_key_id, aws_secret_access_key**

Each CLI command with the flag **--profile workshop** will be to that account.

{{% /expand%}}

### Verify that you have permissions

Verify your client with:
```bash
## windows PowerShell
Get-FSXFileSystem -ProfileName workshop -region eu-west-1

## MacOS CLI
aws fsx describe-file-systems --profile workshop --region eu-west-1
```

Good output:
```bash
PS > Get-FSXFileSystem -ProfileName workshop -region eu-west-1

CreationTime : 4/7/2019 8:38:38 AM
DNSName : fs-08b8d7a080cd06987.domain.name
FailureDetails :
FileSystemId : fs-08b8d7a080cd06987
FileSystemType : WINDOWS
KmsKeyId : arn:aws:kms:eu-west-1:761306897638:key/fd7ea1f9-3a72-4a57-9e06-f7c090248fc5
Lifecycle: AVAILABLE
LustreConfiguration :
NetworkInterfaceIds : {eni-0719ee90e8be02208}
OwnerId : 761306897638
ResourceARN : arn:aws:fsx:eu-west-1:761306897638:file-system/fs-08b8d7a080cd06987
StorageCapacity : 500
SubnetIds : {subnet-00b73284269c627d7}
Tags : {aws:cloudformation:stack-name, aws:cloudformation:logical-id, aws:cloudformation:stack-id,
 ThroughputCapacity...}
VpcId : vpc-00c4f4a70e48874c6
WindowsConfiguration : Amazon.FSx.Model.WindowsFileSystemConfiguration
```