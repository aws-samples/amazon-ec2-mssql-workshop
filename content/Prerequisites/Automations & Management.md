+++
title = "AWS Tools for PowerShell"
date = 2019-03-21T20:40:20+02:00
weight = 4
chapter = false
pre = "<b>4. </b>"
+++

## AWS Tools for Powershell

In this step, you will install AWS Tools on your local machine.

{{%expand "Windows OS" %}} 

1. Run powershell (with Admin shell):

```powershell
## Install the module
Install-Module -Name AWSPowerShell

## Import AWS PowerShell Module
import-module awspowershell

```

See screenshot for how it should look:
![powershell](/img/Steps/aws-powershell-tools.png?classes=border,shadow)

{{% notice note %}}
If the command above isn't working, it's because you are running old PowerShell version, in this case, you can manually download and install [AWS Tools for PowerShell](https://sdk-for-net.amazonwebservices.com/latest/AWSToolsAndSDKForNet.msi). For other troubleshooting, please see the [documentation](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html).
{{% /notice %}}

{{% /expand%}}

{{%expand "macOS" %}} 

### MacOS Users

Most of the scripts and commands that are listed in this workshop are written in Powershell, so if you're using macOS, there are few options:

- Option 1 - Install Powershell - Download and install **full powershell** for macOS from [Microsoft github](https://github.com/PowerShell/PowerShell), then launch the powershell.app from the MacOS launchpad and continue with the workshop. **Using Powershell for macOS you will be able to run commands that are listed in the windows sections (set-awscredential etc..)**

- Option 2 - launch a windows 2019 bastion server, and continue the workshop from the bastion host. 

- Option 3 - Use AWS CLI without PowerShell 

Please note that It's not mandatory to use Powershell for macOS or Bastion host,the workshop commands can work on macOS as well via aws cli, but their syntax will be different 

{{% /expand%}}

### Configure SSH Keys

Set AccessKey, SecretKey and SessionToken to workshop profile

If you are using the account supplied in a workshop, go to https://dashboard.eventengine.run/dashboard and configure your client to work with the account with the following commands:

{{%expand "Windows" %}} 


```powershell

# sets the temporary session-based credentials as active in the current shell. 
Set-AWSCredential -AccessKey AKIAIOSFODNN7EXAMPLE -SecretKey wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY -SessionToken SamPleTokeN -StoreAs workshop

## See the profile
Get-AWSCredential -ListProfileDetail
```

![awscredential](/img/Steps/awscredential.png?classes=border,shadow)

{{% /expand%}}

{{%expand "macOS (without Powershell)" %}} 

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
**Change the aws_access_key_id, aws_secret_access_key and aws_session_token from the workshop dashboard**

Now, each CLI command with the flag **--profile workshop** will be to that account.

{{% /expand%}}


### Verify

Verify your client with:
```bash
## Windows powershell
Get-FSXFileSystem -ProfileName workshop -region eu-west-1

## MacOS CLI
aws fsx describe-file-systems --profile workshop --region eu-west-1
```

Good output:
```bash
PS > Get-FSXFileSystem -ProfileName workshop -region eu-west-1

CreationTime         : 4/7/2019 8:38:38 AM
DNSName              : fs-08b8d7a080cd06987.domain.name
FailureDetails       :
FileSystemId         : fs-08b8d7a080cd06987
FileSystemType       : WINDOWS
KmsKeyId             : arn:aws:kms:eu-west-1:761306897638:key/fd7ea1f9-3a72-4a57-9e06-f7c090248fc5
Lifecycle            : AVAILABLE
LustreConfiguration  :
NetworkInterfaceIds  : {eni-0719ee90e8be02208}
OwnerId              : 761306897638
ResourceARN          : arn:aws:fsx:eu-west-1:761306897638:file-system/fs-08b8d7a080cd06987
StorageCapacity      : 500
SubnetIds            : {subnet-00b73284269c627d7}
Tags                 : {aws:cloudformation:stack-name, aws:cloudformation:logical-id, aws:cloudformation:stack-id,
                       ThroughputCapacity...}
VpcId                : vpc-00c4f4a70e48874c6
WindowsConfiguration : Amazon.FSx.Model.WindowsFileSystemConfiguration
```