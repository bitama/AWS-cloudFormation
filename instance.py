import boto3

resource=boto3.client("ec2")
def createInstance():
        try:
                resource.run_instances(
                ImageId="ami-0b0dcb5067f052a63", 
                MinCount=1,
                MaxCount=1,
                InstanceType="t2.micro",
                KeyName="my-key-pair" 
                )
        except Exception as e:
                print(e)
def decribeInstance():
        print(resource.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"]
        # [0]['Instances'][0]
        # ['InstanceId']
        )

createInstance()
decribeInstance()

