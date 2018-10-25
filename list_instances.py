import pprint
import subprocess

import boto3

# Declaring EC2 variable
ec2 = boto3.resource('ec2')

try:
    # Retrieving a filtered list of instances
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for i in instances:
        print("Instance Id: " + i.id + ", Instance IP Address: " + i.public_ip_address)

        cmd = "ssh -i devops.pem ec2-user@" + i.public_ip_address + " 'python3 check_webserver.py'"

        output = subprocess.run(cmd, check=True, shell=True)
        pprint.pprint(output)

except Exception as error:
    print(error)
