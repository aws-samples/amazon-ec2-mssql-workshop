<powershell>
# Create pool and virtual disk for DB files using parity with EBS, ReFS 64K, D: Drive
$EBS = Get-PhysicalDisk | ? { $_.CanPool -eq $True -and $_.FriendlyName -eq "NVMe Amazon Elastic B" -and $_.Size -ne 150000000000}
New-StoragePool –FriendlyName DBPool –StorageSubsystemFriendlyName "Windows Storage*" –PhysicalDisks $EBS
New-VirtualDisk -StoragePoolFriendlyName DBPool -FriendlyName DBDisk -ResiliencySettingName mirror -ProvisioningType Fixed -UseMaximumSize
Get-VirtualDisk –FriendlyName DBDisk | Get-Disk | Initialize-Disk –Passthru | New-Partition –DriveLetter D –UseMaximumSize | Format-Volume -FileSystem ReFS -AllocationUnitSize 65536 -NewFileSystemLabel DBfiles -Confirm:$false
 
# Create pool and virtual disk for TempDB using the local NVMe, ReFS 64K, E: Drive
$NVMe = Get-PhysicalDisk | ? { $_.CanPool -eq $True -and $_.FriendlyName -eq "NVMe Amazon EC2 NVMe"}
New-StoragePool –FriendlyName TempDBPool –StorageSubsystemFriendlyName "Windows Storage*" –PhysicalDisks $NVMe
New-VirtualDisk -StoragePoolFriendlyName TempDBPool -FriendlyName TempDBDisk -ResiliencySettingName simple -ProvisioningType Fixed -UseMaximumSize
Get-VirtualDisk –FriendlyName TempDBDisk | Get-Disk | Initialize-Disk –Passthru | New-Partition –DriveLetter E –UseMaximumSize | Format-Volume -FileSystem ReFS -AllocationUnitSize 65536 -NewFileSystemLabel TempDBfiles -Confirm:$false

# Create a startup script to handle NVMe refresh on start/stop instance
$bootfix = {
    if (!(Get-Volume -DriveLetter E)) {
        #Create pool and virtual disk for TempDB using mirroring with NVMe
        $NVMe = Get-PhysicalDisk | ? { $_.CanPool -eq $True -and $_.FriendlyName -eq "NVMe Amazon EC2 NVMe"}
        New-StoragePool –FriendlyName TempDBPool –StorageSubsystemFriendlyName "Windows Storage*" –PhysicalDisks $NVMe
        New-VirtualDisk -StoragePoolFriendlyName TempDBPool -FriendlyName TempDBDisk -ResiliencySettingName simple -ProvisioningType Fixed -UseMaximumSize
        Get-VirtualDisk –FriendlyName TempDBDisk | Get-Disk | Initialize-Disk –Passthru | New-Partition –DriveLetter E –UseMaximumSize | Format-Volume -FileSystem ReFS -AllocationUnitSize 65536 -NewFileSystemLabel TempDBfiles -Confirm:$false

        #grant Everyone full access to the new drive
        $item = gi -literalpath "E:\"
        $acl = $item.GetAccessControl()
        $permission="Everyone","FullControl","Allow"
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
        $acl.SetAccessRule($rule)
        $item.SetAccessControl($acl)
    
        #gRestart SQL so it can create tempdb on new drive
        Stop-Service SQLSERVERAGENT
        Stop-Service MSSQLSERVER
        Start-Service SQLSERVERAGENT
        Start-Service MSSQLSERVER
        }
}
 
New-Item -ItemType Directory -Path c:\Scripts    
$bootfix | set-content c:\Scripts\bootfix.ps1
 
# Create a scheduled task on startup to execute script if required (if E: is lost)
$action = New-ScheduledTaskAction -Execute 'Powershell.exe' -Argument 'c:\scripts\bootfix.ps1'
$trigger =  New-ScheduledTaskTrigger -AtStartup 
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Rebuild TempDBPool" -Description "Rebuild TempDBPool if required" -RunLevel Highest -User System
</powershell>
