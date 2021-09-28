import boto3


# user keys
print("\nAuto Scale Group Creation\n\nAWS Account keys:")
access_key = input("Input Access Key: ")
secret_key = input("Input Secret Key: ")
client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# prints available regions and requesting user choice.
print("\nListing available regions: ")
available_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
for i, region in enumerate(available_regions, start=1):
    print(f'{i}) {region}')
region_choice = available_regions[int(input("\nChoose Region: ")) - 1]
print("You Chose:", region_choice)

# config region based on user choice.
client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_choice)

# prints available VPC's and requesting user choice.
print("\nListing available VPC's: ")
vpcs = [vpc['VpcId'] for vpc in client.describe_vpcs()['Vpcs']]
for i, vpc in enumerate(vpcs, start=1):
    print(f'{i}) {vpc}')
vpc_id = vpcs[int(input("\nChoose VPC Id: ")) - 1]
print("You Chose:", vpc_id)

# prints available subnets (based on VPC choice) and requesting user choice.
subnets = [(subnet['SubnetId'], subnet['Tags'][0]['Value']) for subnet in client.describe_subnets(Filters=[dict(Name='vpc-id', Values=[str(vpc_id)])])['Subnets']]
print("\nListing available subnets: ")
for i, (subnet_id, subnet_name) in enumerate(subnets, start=1):
    print(f'{i}) {subnet_id} - {subnet_name}')
subnet_ids = input("\nChoose which Subnets will you use (i.e. 1, 8, 12): ")
subnets = [subnets[int(index.strip()) - 1] for index in subnet_ids.split(',')]
VPCZoneId_filtered = {subnet[0] for subnet in subnets}
print("You Chose:")
for subnet_id, subnet_name in subnets:
    print(subnet_id, subnet_name)

# request versions.
lt_v_amount = input("\nSpecify the Launch Template versions you will use (i.e. 1, 8, 12):")
lt_v_amountw = str([lt_v_amount[int(index.strip()) -1] for index in lt_v_amount.split(',')])
print("test1", lt_v_amountw)
for i, version_num in enumerate(lt_v_amountw, start=1):
    print(f'{i} {version_num}')

print("test2", version_num[0])

# print available render types in chosen region.
available_render_types = [render['InstanceType'] for render in client.describe_instance_type_offerings(LocationType="region", Filters=[dict(Name='location', Values=[str(region_choice)]), dict(Name='instance-type', Values=['g*', 'p*'])])['InstanceTypeOfferings']]
print("\nListing available rendering Types for chosen region: ")
for i, instance_type in enumerate(available_render_types, start=1):
    print(f'{i}) {instance_type}')
render_types = input("\nChoose instance types you will use (i.e. 1, 8, 12): ")
available_render_types = [available_render_types[int(index.strip()) - 1] for index in render_types.split(',')]
print("\nYou Chose:")
for render_type in available_render_types:
    print(render_type)

# starting scaling parameters
minimum = int(input("\nPlease choose minimum capacity: "))
maximum = int(input("Please choose maximum capacity: "))
desired = int(input("Please choose desired capacity: "))

client = boto3.client('autoscaling', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_choice)

# prompting user to choose AutoScale Group name, Launch Template name and the amount of versions he will use from LT.
asg_name = str(input("\nChoose Auto Scale Group Name: "))
lt_name = str(input("Input Existing Launch Template Name: "))

# ASG creation process.
create_autoscale_group = client.create_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    MixedInstancesPolicy={
        'LaunchTemplate': {
            'LaunchTemplateSpecification': {
                'LaunchTemplateName': lt_name,
                'Version': version_num[0]
            },
            'Overrides': [
                {
                    'InstanceType': render_type[0],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[0]
                    }
                },
                {
                    'InstanceType': render_type[1],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[1]
                    }
                },
                {
                    'InstanceType': render_type[2],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[2]
                    }
                },
                                {
                    'InstanceType': render_type[3],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[3]
                    }
                },
                                {
                    'InstanceType': render_type[4],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[4]
                    }
                },
                                {
                    'InstanceType': render_type[5],
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': lt_name,
                        'Version': version_num[5]
                    }
                },
            ]
        },
        'InstancesDistribution': {
            'OnDemandBaseCapacity': 0,
            'OnDemandPercentageAboveBaseCapacity': 0,
            'SpotAllocationStrategy': 'capacity-optimized',
        }
    },
    MinSize=minimum,
    MaxSize=maximum,
    DesiredCapacity=desired,
    VPCZoneIdentifier=VPCZoneId_filtered,
    Tags=[
        {
            'ResourceId': asg_name,
            'ResourceType': 'auto-scaling-group',
            'Key': 'Name',
            'Value': asg_name,
            'PropagateAtLaunch': True
        },
    ],
)

print(create_autoscale_group)
