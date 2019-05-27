+++
title = "AWS Systems Manager"
date = 2019-03-21T20:40:20+02:00
weight = 5
chapter = false
pre = "<b>5. </b>"
+++


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

Use the following script, to automate the process of sending powershell commands and wait for their output.

**Please read the script and make sure you understand the logic**

Download the following script locally:

```powershell
# Gets Instance ids and list of commands and returns the output

## Define parameters
param (
    [string]$region = "eu-west-1",
    [Parameter(Mandatory=$true)][string[]]$instanceids,
    [Parameter(Mandatory=$true)][string[]]$commands,
	[bool]$IsLinux = $false,
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

**Save this script locally with the name runcommand.ps1**

{{% notice note %}}
In the next steps you will launch 2 instances, then use this script to send commands remotely and easly.
{{% /notice %}}

Syntax:

```powershell
.\runcommand.ps1 -instanceids instance_id_1,instance_id_2 -commands "Some commands" -region "eu-west-1" -profile "workshop" -IsLinux $False
```

Example:

I ran the following command from my local machine to remotely execute the "ipconfig" command on the instance id i-0c47c2bbbc7864277. In the next step, you will launch instances, and use the script in the same way to run other commands.

```powershell
.\runcommand.ps1 -instanceids i-0c47c2bbbc7864277 -commands "ipconfig" -region eu-west-1 -profile "workshop" -IsLinux $false
```
![powershell](/img/Steps/runcommandscript.png?classes=border,shadow)
