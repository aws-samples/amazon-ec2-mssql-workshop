+++
title = "Automations & Management"
date = 2019-03-21T20:40:20+02:00
weight = 4
chapter = false
pre = "<b>4. </b>"
+++

## AWS Tools for Powershell

In this step, we are going to use AWS Tool for Powershell, and a script provided, to send commands to remote servers, and wait for their output.
Please make sure that your machine is configured with a IAM keys.

**Users who are running powershell 5.0 or newer, can install Tools for Powershell from Microsoft's Gallery by running "Install-Module -Name AWSPowerShell" (with Admin shell)**

If the command isn't working, please download and install [AWS Tools for PowerShell](https://sdk-for-net.amazonwebservices.com/latest/AWSToolsAndSDKForNet.msi)

For troubleshooting, please see the [documentation](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html).

List of commands to install Powershell on your computer:

```powershell
## Open CMD and run Powershell
powershell

## Install AWS Powershell
Install-Module -Name AWSPowerShell


## Import AWS PowerShell Module
import-module awspowershell

#Sets the temporary session-based credentials as active in the current shell. Note that temporary credentials cannot be saved as a profile.
Set-AWSCredential -AccessKey AKIAIOSFODNN7EXAMPLE -SecretKey wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY -SessionToken SamPleTokeN -StoreAs workshop

## See the profile
Get-AWSCredential -ListProfileDetail
```

- Verify your client is configured correctly with the command "Get-AWSPowerShellVersion -ListServiceVersionInfo"

{{% notice note %}}
If you're using macOS, and you want to use the script provided in this workshop, launch windows 2019 bastion server, and continue the workshop from the bastion host. But it's not mandatory, the commands can work on macOS as well (but without the script, you will need to it manually)
{{% /notice %}}


## Create IAM user and SSH Keys

**This step is not relevant if you are using Event Engine Account!**


- Configure your client to work with [AWS Credentials](https://docs.aws.amazon.com/powershell/latest/userguide/specifying-your-aws-credentials.html) 

{{% notice note %}}
If you are using the account supplied in workshop, go to https://dashboard.eventengine.run/dashboard and configure your client to work with the account.
{{% /notice %}}

If you are run the workshop on your own account:

- Open the IAM console.
- On the navigation menu, choose Users.
- Choose your IAM user name (not the check box).
- Open the Security credentials tab, and then choose "Create access key".
- To see the new access key, choose "Show".


**It's higly recommended setting a new CLI profile:**

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


Verify your client with:
```
Get-FSXFileSystem -ProfileName workshop -region eu-west-1
```

Good output:
```
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

---------------

## AWS Systems Manager

AWS Systems Manager is a collection of capabilities for configuring and managing your Amazon EC2 instances, on-premises servers and virtual machines, and other AWS resources at scale. Systems Manager includes a unified interface that allows you to easily centralize operational data and automate tasks across your AWS resources. Systems Manager shortens the time to detect and resolve operational problems in your infrastructure. Systems Manager gives you a complete view of your infrastructure performance and configuration, simplifies resource and application management, and makes it easy to operate and manage your infrastructure at scale.

### Run-command

See AWS Run-command: https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html 

**Question:**
How to use the Send-SSMCommand to send powershell script using SSM Agent that already installed (by default) on the instances?

{{%expand "See hint" %}} 
Hint: (Send-SSMCommand powershell command https://docs.aws.amazon.com/powershell/latest/reference/items/Send-SSMCommand.html)
{{% /expand%}}

{{%expand "See answer" %}} 
**Answer:**

The syntax for running single powershell command on instance is:
```powershell
Send-SSMCommand -InstanceId $id -DocumentName AWS-RunPowerShellScript -Comment 'Comment' -Parameter @{commands = $command_or_commands} -region $region
```
{{% /expand%}}

{{% notice note %}}
The DocumentName is set to AWS-RunPowerShellScript, to read more and see different type of documents see: https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-plugins.html
{{% /notice %}}

**Question:**
How to see the output of the command? 

{{%expand "See answer" %}} 
**Answer:**
To see the output or the progress of the commands , we can use the **Get-SSMCommandInvocation** command


**Example:**
```powershell
Get-SSMCommandInvocation -CommandId $runPSCommand.CommandId -Details $true -InstanceId $instanceid -region $region
```
{{% /expand%}}

### Script

Use the following script, to automate the process of sending powershell command and wait for the output from the instances.

**Please read the script and make sure you understand the logic**

Download the following script locally 

```powershell
# Gets Instance ids and list of commands and returns the output

## Define parameters
param (
    [string]$region = "eu-west-1",
    [Parameter(Mandatory=$true)][string[]]$instanceids,
    [Parameter(Mandatory=$true)][string[]]$commands,
	[bool]$IsLinux = $false
    [string]$profile = "workshop"
 )

## **** Send commands **** ##

Write-Output "Creating the document on" $instanceids
$DocumentName = "AWS-RunPowerShellScript"
if ($IsLinux -eq $true)
{
	$DocumentName = "AWS-RunShellScript"
}
## Runs the command on all the instances 
$runPSCommand= Send-SSMCommand -InstanceId $instanceids -DocumentName $DocumentName -Comment 'Script to run powershell commands' -Parameter @{commands = $commands} -region $region -ProfileName $profile

sleep(1)

## **** Waiting for output from the instances **** 

## Invoke the command on each instance
foreach ($instanceid in $instanceids)
    {
    ## Print nice UI
    Write-Output "------------------------------------"
    Write-Output "Working on: $instanceid"
    Write-output "`n *****Output from the instance:***** `n"

    ## Get Status of the invocation
    $status = Get-SSMCommandInvocation -CommandId $runPSCommand.CommandId -Details $true -InstanceId $instanceid -region $region -ProfileName $profile | select -ExpandProperty CommandPlugins | select Status

    ## Wait until the command is invoked successfully
    while ($status.Status -eq 'InProgress')
        {
        sleep(1)
        $status = Get-SSMCommandInvocation -CommandId $runPSCommand.CommandId -Details $true -InstanceId $instanceid -region $region -ProfileName $profile | select -ExpandProperty CommandPlugins | select Status
        }
    
    ## Get the output from the instance(s)
    Get-SSMCommandInvocation -CommandId $runPSCommand.CommandId -Details $true -InstanceId $instanceid -region $region -ProfileName $profile | select -ExpandProperty CommandPlugins | select  -ExpandProperty Output

    ## Print nice ui
    Write-output "`n *****End of output from the instance***** `n"
    }

## Print nice ui
Write-Output "------------------------------------"
Write-Output "Done"
```

- Save this script locally with the name runcommand.ps1

{{% notice note %}}
In the next steps you are going to launch instances, then use this script to send commands remotely and easly.
{{% /notice %}}

Example of usage:

```powershell
.\runcommand.ps1 -instanceids instance_id_1,instance_id_2 -commands "Some commands" -region "eu-west-1" -profile "workshop"
```