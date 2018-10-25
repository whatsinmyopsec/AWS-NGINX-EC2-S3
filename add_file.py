#!/usr/bin/env python3

import pprint
import subprocess
import webbrowser

import boto3

s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')


# This is to make sure nothing breaks really
def countdown(n):
    import time
    pprint.pprint('This will now go for more seconds...')
    while n >= 0:
        print(n, end='...')
        time.sleep(1)
        n -= 1
    print('Next step \n')


def add_file():
    try:

        for bucket in s3.buckets.all():
            print(bucket.name)
            print("----------------")
            for item in bucket.objects.all():
                print("\t%s" % item.key)

    except Exception as errors:
        print(errors)

    bucket = input('\nPlease type in the name of the bucket you wish to choose a file from: ')
    picture = input('\nPlease type in the name of the image you uploaded: ')

    # Indentation matters // not really

    # create the index page
    def createindex():
        htmlfile = open("index.html", "w+")

        htmlfile.write('<img src="https://s3-eu-west-1.amazonaws.com/' + bucket + '/' + picture + '"/>')

        htmlfile.close()

    try:
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print("Instance Id: " + instance.id + ", Instance IP Address: " + instance.public_ip_address)

            createindex()
            print('index.html has been created')

            # Copy index page to server
            cmd_scp = "scp -i devops.pem index.html ec2-user@" + instance.public_ip_address + ":."
            print('index uploaded')
            countdown(10)
            output = subprocess.run(cmd_scp, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(output)

            cmd = "ssh -i devops.pem ec2-user@" + instance.public_ip_address + " 'cd /usr/share/nginx/html; " \
                                                                               "sudo rm -f index.html; " \
                                                                               "cd ~; " \
                                                                               "sudo mv index.html /usr/share/" \
                                                                               "nginx/html/index.html'"
            countdown(10)
            output = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(output)

            print('opening in the best web browser')
            webbrowser.open_new(instance.public_ip_address)

    except Exception as error:
        print(error)


# Define a main() function
def main():
    add_file()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
