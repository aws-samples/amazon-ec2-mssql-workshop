import boto3
import argparse
import json

parser = argparse.ArgumentParser(description='Helper tool to generate Amazon CloudWatch Dashboard with all EBS volumes attached to the instances and their important metrics')
parser.add_argument("--region", type=str, help="Set the region where the instances are running. Default is us-east-1", nargs='?', default='us-east-1')
parser.add_argument("--profile", type=str, help="Local AWS profile to use, leave empty for default profile", nargs='?', default="")
parser.add_argument("--InstanceList", default=[], help="<Required> Add here all the instance types that you want to monitor (i.e: 'i-example i-example2''", nargs='+', required=True)
parser.add_argument("--DashboardName" , type=str ,help="Set the cloudwatch dashboard name you want to create using this CLI. Please note that in case you specify a name that already exists, it will override the dashboard.", default='EC2-EBS-Monitor', nargs='?')

args = parser.parse_args()

# Vars
region = args.region
profile = args.profile
InstanceList = args.InstanceList
CloudWatch_DashboardName = args.DashboardName

# Do not edit from here

if profile != "":
    account = boto3.setup_default_session(profile_name = profile)

ec2 = boto3.resource('ec2', region_name=region)
cw = boto3.client('cloudwatch', region_name=region)
ec2client = boto3.client('ec2', region_name=region)

def get_ebs(instance_id):
    instance = ec2.Instance(instance_id)
    volumes = instance.volumes.all()
    ebs_list = [v.id for v in volumes]
    return ebs_list

def get_speed(instances):
    answer_from_ec2_client = ec2client.describe_instance_types(InstanceTypes=instances)
    network_per_instance = {
        "InstanceTypes": {}
    }
    for instance in answer_from_ec2_client['InstanceTypes']:
        instance_details = {
            instance['InstanceType']: {
                "EbsInfo" : instance['EbsInfo'],
                "NetworkInfo": instance['NetworkInfo']
            }
        }
        network_per_instance['InstanceTypes'].update(instance_details)
    return network_per_instance

def get_instance_name(instance_id):
    ec2instance = ec2.Instance(instance_id)
    instancename = ' '
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return instancename

def create_cw_dashboard(ec2_list, networklimit):
    widgets = {"widgets": []}
    number = 1
    # EBS to the EC2
    for ec2instance in ec2_list:
        instance_name = get_instance_name(ec2instance)
        ec2instance_type = ec2.Instance(ec2instance)
        ec2_details = ec2client.describe_instance_types(InstanceTypes=[ec2instance_type.instance_type])
        ebs_volumes = get_ebs(ec2instance) ## get all EBS volumes per instance

        ## New instance Header
        new_widget = {
            "type": "text",
            "width": 24,
            "height": 4,
            "properties": {
                "markdown": f'\n# Report #{number}\
                            \n\n**Instance ID:** {ec2instance} \
                            \n\n**Tag:Name:** {instance_name} \
                            \n\n**InstanceType:** {ec2instance_type.instance_type} \
                            \n\n**Attached Volumes:** {ebs_volumes}'
            }
        }
        widgets['widgets'].append(new_widget)

        ## Instance -> Internet Gateway
        new_widget = {
            "type": "text",
            "width": 24,
            "height": 2,
            "properties": {
                "markdown": "\n## " + "EC2 (" + ec2instance_type.instance_type + ") --> " + "Network" +"\n"
            }
        }
        widgets['widgets'].append(new_widget)
        ec2_NetworkInfo = ec2_details['InstanceTypes'][0]['NetworkInfo']
        # Extract the number
        numbers = []
        for word in ec2_NetworkInfo['NetworkPerformance'].split():
            if word.isdigit():
                numbers.append(int(word))

        # EC2 Metrics 
        new_widget = {
            "type": "metric",
            "width": 24,
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS('network'))/PERIOD(networkOut)", "label": "Bandwidth (Bytes)", "id": "bandwidthBytes", "visible": False , "period": 300} ], 
                    [ { "expression": "bandwidthBytes*0.000008", "label": "Bandwidth (Mbps - Megabits)", "id": "bandwidthMbps" , "period": 300} ], # Convert Bytes to Megabits -> 1 B = 0.000008 Mb
                    [ "AWS/EC2", "NetworkIn", "InstanceId", ec2instance, { "visible": False, "id": "networkIn", "period": 300 } ],
                    [ "AWS/EC2", "NetworkOut", "InstanceId", ec2instance, { "visible": False, "id": "networkOut" , "period": 300} ]
                ],
                "view": "timeSeries",
                "stacked": False,
                "region": region,
                "stat": "Sum",
                "period": 300,
                "title": ec2instance + " --> Network",
                "annotations": {
                    "horizontal": [
                        {
                            "label": "Maximum Throughput (Mbps)",
                            "value": numbers[0]*1000
                        }
                    ]
                }
            }
        }
        widgets['widgets'].append(new_widget)


        ## Instance -> EBS
        new_widget = {
            "type": "text",
            "width": 24,
            "height": 2,
            "properties": {
                "markdown": "\n## " + "Amazon EC2" + " --> " + "Amazon EBS" +"\n"
            }
        }
        widgets['widgets'].append(new_widget)
        if(networklimit['InstanceTypes'][ec2instance_type.instance_type]['EbsInfo']['EbsOptimizedSupport'] != 'unsupported'):
            network_to_ebs = networklimit['InstanceTypes'][ec2instance_type.instance_type]['EbsInfo']['EbsOptimizedInfo']['MaximumBandwidthInMbps']
            network_to_ebs_half = network_to_ebs*0.5
            network_to_ebs_iops = networklimit['InstanceTypes'][ec2instance_type.instance_type]['EbsInfo']['EbsOptimizedInfo']['MaximumIops']
            network_to_ebs_iops_half = network_to_ebs_iops*0.5
        else:
            network_to_ebs = 0
            network_to_ebs_half = 0
            network_to_ebs_iops = 0
            network_to_ebs_iops_half = 0
        new_widget = {
            "type": "metric",
            "width": 12,
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS('ebs'))/PERIOD(ebsReadBytes)", "label": "Total IO In Bytes", "id": "totalIOBytes", "visible": False , "period": 300 } ], # (ebsReadBytes + ebsWriteBytes) / Period
                    [ { "expression": "totalIOBytes*0.000008", "label": "Bandwidth (Mbps - Megabits)", "id": "bandwidthMbps" , "period": 300} ], # Convert Bytes to Megabits -> 1 B = 0.000008 Mb
                    [ "AWS/EC2", "EBSReadBytes", "InstanceId", ec2instance, { "visible": False, "id": "ebsReadBytes", "period": 300 } ],
                    [ ".", "EBSWriteBytes", ".", ".", { "visible": False, "id": "ebsWriteBytes", "period": 300 } ]
                ],
                "view": "timeSeries",
                "stacked": False,
                "region": region,
                "stat": "Sum",
                "period": 300,
                "title": ec2instance + " -> EBS (Throughput)",
                "annotations": {
                    "horizontal": [
                        {
                            "label": "Maximum Throughput (Mbps)",
                            "value": network_to_ebs
                        },
                        {
                            "label": "50% Throughput (Mbps)",
                            "value": network_to_ebs_half
                        }
                    ]
                }
            }
        }
        widgets['widgets'].append(new_widget)

        new_widget = {
            "type": "metric",
            "width": 12,
            "properties": {
                "metrics": [
                    [ { "expression": "SUM(METRICS('ebs'))/PERIOD(ebsWriteOps)", "label": "Total IOPS", "id": "totalIOPS", "visible": True , "period": 300 } ], 
                    [ "AWS/EC2", "EBSWriteOps", "InstanceId", ec2instance, { "visible": False, "id": "ebsReadOps", "period": 300 } ],
                    [ ".", "EBSReadOps", ".", ".", { "visible": False, "id": "ebsWriteOps", "period": 300 } ]
                ],
                "view": "timeSeries",
                "stacked": False,
                "region": region,
                "stat": "Sum",
                "period": 300,
                "title": ec2instance + " -> Amazon EBS (IOPS)",
                "annotations": {
                    "horizontal": [
                        {
                            "label": "Maximum IOPS",
                            "value": network_to_ebs_iops
                        },
                        {
                            "label": "50% IOPS",
                            "value": network_to_ebs_iops_half
                        }
                    ]
                }
            }
        }
        widgets['widgets'].append(new_widget)

        ## EBS -> Instance
        new_widget = {
            "type": "text",
            "width": 24,
            "height": 2,
            "properties": {
                "markdown": "\n## Amazon EBS --> Amazon EC2 \n"
            }
        }
        widgets['widgets'].append(new_widget)

        for volume in ebs_volumes:
            volume_speed = ec2.Volume(volume)
            new_widget = {
                "type": "text",
                "width": 24,
                "height": 2,
                "properties": {
                    "markdown": "\n### InstanceID: " +ec2instance + " Volume: "+ volume +" ("+volume_speed.volume_type +")\n"
                }
            }
            widgets['widgets'].append(new_widget)
            ## Volume Throughput
            new_widget = {
                "type": "metric",
                "width": 12,
                "properties": {
                    "metrics": [
                        [ { "expression": "SUM(METRICS('volume'))/PERIOD(volumeReadBytes)", "label": "Total IO (Bytes)", "id": "volumeThroughputBytes", "visible": False, "stat": "Sum", "period": 300 } ],
                        [ { "expression": "volumeThroughputBytes/1024/1024", "label": "Total Throughput (MB/s - MegaBytes per second)", "id": "volumeThroughputMBps", "stat": "Sum", "period": 300 } ], 
                        [ "AWS/EBS", "VolumeWriteBytes", "VolumeId", volume, { "visible": False, "id": "volumeWriteBytes", "period": 300 } ],
                        [ "AWS/EBS", "VolumeReadBytes", "VolumeId", volume, { "visible": False, "id": "volumeReadBytes", "period": 300 } ]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": region,
                    "stat": "Sum",
                    "period": 300,
                    "yAxis": {
                        "left": {
                            "showUnits": False,
                            "label": "MiB/s"
                        },
                        "right": {
                            "showUnits": False
                        }
                    },
                    "title": "Throughput" + "(" + volume +")"
                }
            }

            # Add space for annotations
            new_widget['properties'].update({'annotations': {'horizontal': []}})
            flagForIOPS = True

            if volume_speed.volume_type == "gp2":
                if (volume_speed.size < 170):
                    new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps)","value": 128})
                if (volume_speed.size > 170 and volume_speed.size < 334):
                    new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps) ** (if burst credits are available)","value": 250})
                if (volume_speed.size > 334):
                    new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps)","value": 250})
            if volume_speed.volume_type == "io2" or volume_speed.volume_type == "io1":
                new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps)","value": 1000})
            if volume_speed.volume_type == "st1":
                new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps)","value": 500})
                flagForIOPS = False
            if volume_speed.volume_type == "sc1":
                new_widget['properties']['annotations']['horizontal'].append({"label": "Maximum Throughput (MBps)","value": 250})
                flagForIOPS = False
            if  volume_speed.volume_type == "gp3":
                if(volume_speed.throughput == 125):
                    new_widget['properties']['annotations']['horizontal'].append({"label": "Baseline Throughput (MBps)","value": 125})
                else:
                    new_widget['properties']['annotations']['horizontal'].append({"label": "Provisioned Throughput (MBps)","value": volume_speed.throughput})

            widgets['widgets'].append(new_widget)
            iopsValue = 0

            if bool(flagForIOPS):
                iopsValue = volume_speed.iops
            else:
                iopsValue = 0

            # Volume IOPS
            new_widget = {
                "type": "metric",
                "width": 12,
                "properties": {
                    "metrics": [
                        [ { "expression": "SUM(METRICS('volume'))/PERIOD(volumeReadOps)", "label": "Total IOPS (Operations Per Second)", "id": "totalIOPS", "stat": "Sum", "period": 300 } ],
                        [ "AWS/EBS", "VolumeWriteOps", "VolumeId", volume, { "visible": False, "id": "volumeWriteOps", "period": 300 } ],
                        [ "AWS/EBS", "VolumeReadOps", "VolumeId", volume, { "visible": False, "id": "volumeReadOps" , "period": 300} ]
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": region,
                    "stat": "Sum",
                    "period": 300,
                    "yAxis": {
                        "left": {
                            "showUnits": False,
                            "label": "IOPS"
                        },
                        "right": {
                            "showUnits": False
                        }
                    },
                    "title": "IOPS" + "(" + volume +")",
                    "annotations": {
                    "horizontal": [
                        {
                            "label": "Baseline performance - IOPS",
                            "value": iopsValue
                        }
                    ]
                }
                }
            }
            if volume_speed.volume_type == "gp2":
                new_widget['properties']['annotations']['horizontal'].append({"label": "Burst IOPS","value": 3000})
            if volume_speed.volume_type == "gp3" and iopsValue != 3000:
                new_widget['properties']['annotations']['horizontal'].append({"label": "Burst IOPS","value": 3000})
            widgets['widgets'].append(new_widget)
        number += 1

    dashboard = {"periodOverride": "inherit", "widgets": widgets['widgets']}
    result = cw.put_dashboard(DashboardName=CloudWatch_DashboardName,DashboardBody=json.dumps(dashboard))
    print(result)

def get_instance_type_from_ids(instances):
    list_of_instance_types = []

    for instance in instances:
        ec2instance = ec2.Instance(instance)
        instance_type = ec2instance.instance_type
        if(instance_type not in list_of_instance_types):
            list_of_instance_types.append(instance_type)

    return list_of_instance_types


Instance_Speed = get_speed(get_instance_type_from_ids(InstanceList))

create_cw_dashboard(InstanceList,Instance_Speed)