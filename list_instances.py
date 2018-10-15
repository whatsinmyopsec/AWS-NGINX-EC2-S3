import subprocess

import boto3

# Declaring EC2 variable
ec2 = boto3.resource('ec2')

try:
    # Retrieving a List of instances
    for instance in ec2.instances.all():
        print(instance.id, instance.state, instance.public_ip_address)

        cmd = "ssh -i devops.pem ec2-user@" + instance.public_ip_address + " 'python3 check_webserver.py'"

        output = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(output)

except Exception as error:
    print(error)
