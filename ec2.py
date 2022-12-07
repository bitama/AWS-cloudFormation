import boto3
import threading
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2", region_name="us-east-1")
myEc2 = input("Create instance: ")
response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')


try:
    response = ec2.create_security_group(GroupName='SECURITY_GROUP_NAME',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    # print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    # print('Ingress Successfully Set %s' % data)

except ClientError as e:
    if str(e).__contains__('already exists'):
        response = ec2.describe_security_groups(
            GroupNames=["SECURITY_GROUP_NAME"])
        security_group_id = response["SecurityGroups"][0]['GroupId']
    else:
        pass
       # print(e)

try:
    response = ec2.create_key_pair(
        KeyName='my-key-pair',
    )
except:
    Key = "my-key-pair"


def create_instance():
    ec2.run_instances(
        ImageId="ami-0b0dcb5067f052a63",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName=Key,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': myEc2
                        }]}])


create_instance()

res = ec2.describe_instances()
print("_______________________________________________________________________________________________________________")


def runIt():
    threading.Timer(10.0, runIt).start()
    for reservation in res["Reservations"]:
        for instance in reservation["Instances"]:
            if instance['State']["Name"] == "running":
                print("The instance is running")
            elif instance['State']["Name"] == "pending":
                print("The instance is pending")
            else:
                print("There is not running or pending instance")
                break

    runIt()


def stopInstance():
    newList = []
    for reservation in res["Reservations"]:
        for instance in reservation["Instances"]:
            newList.append(instance['InstanceId'])
            ec2.terminate_instances(InstanceIds=newList)


stopInstance()
