#!/usr/bin/env python3

import pprint
import subprocess

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
    picture = input('\nPlease type in the name of the file you wish to copy to the Index page: ')

    # Indentation matters // not really

    # create the index page
    def createindex():
        htmlfile = open("index.html", "w+")

        htmlfile.write('<img src="https://s3-eu-west-1.amazonaws.com/' + bucket + '/' + picture + '"/>')

        htmlfile.close()

    try:
        for instance in ec2.instances.all():
            print(instance.id, instance.state, instance.public_ip_address)

            createindex()
            print('index.html has been created')
            countdown(5)

            # Copy index page to server
            cmd_scp = "scp -i devops.pem index.html ec2-user@" + instance.public_ip_address + ":."
            countdown(10)
            output = subprocess.run(cmd_scp, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pprint.pprint(output)

            # set index page on nginx server
            cmd = "ssh -i devops.pem ec2-user@" + instance.public_ip_address + \
                  " 'mv index.html /usr/share/nginx/html '"
            countdown(10)
            output = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pprint.pprint(output)

    except Exception as error:
        print(error)


# Define a main() function
def main():
    add_file()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
