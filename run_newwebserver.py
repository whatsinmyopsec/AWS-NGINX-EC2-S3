import subprocess
import time

import boto3

# Declaring EC2 variable
ec2 = boto3.resource('ec2')


# Creates a new instance
def create_instance():
    # Ask the user to give the new instance a name
    instancename = input('Please give your new instance a name: ')
    tags = [{'Key': 'Name', 'Value': instancename}]
    tag_spec = [{'ResourceType': 'instance', 'Tags': tags}]

    # try/except so the script will not crash
    try:
        instance = ec2.create_instances(
            ImageId='ami-047bb4163c506cd98',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='devops',
            TagSpecifications=tag_spec,
            SecurityGroupIds=['sg-0d2d781ed4f0610db'],
            # UserData that will be executed on creation of the instance
            UserData='''#!/bin/bash
                     sudo yum -y update
                     sudo yum -y install python36
                     yum -y install nginx1.12
                     service nginx start
                     chkconfig nginx on
                      touch home/ec2-user/testFile''')

        print("An EC2 instance with ID", instance[0].id, "has been created.")
        time.sleep(5)
        instance[0].reload()
        print("Public IP address:", instance[0].public_ip_address)

        # Suppress the new host key confirmation prompt and allow SSH remote command execution
        cmd = "ssh -o StrictHostKeyChecking=no -i devops.pem ec2-user@" + instance[0].public_ip_address + " 'pwd'"
        time.sleep(60)
        (status, output) = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(output)

        # SCP the check_webserver.py file to the instance
        cmd_scp = "scp -i devops.pem ~/PycharmProjects/devops-assign-1/check_webserver.py ec2-user@" + instance[
            0].public_ip_address + ":."
        (status, output) = subprocess.run(cmd_scp, check=True, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        print(output)

    except Exception as error:
        print(error)


# Define a main() function
def main():
    create_instance()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
