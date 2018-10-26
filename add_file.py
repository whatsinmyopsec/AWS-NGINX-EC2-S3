#!/usr/bin/env python3

import subprocess
import time
import webbrowser

import boto3
from tqdm import tqdm

s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')


# This is to make sure nothing breaks really
def progress(m):
    pbar = tqdm(total=m)
    for i in range(m):
        time.sleep(1)
        pbar.update(1)
    pbar.close()


def add_file():
    try:

        for bucket in s3.buckets.all():
            print(bucket.name)
            print("----------------")
            for item in bucket.objects.filter():
                print("\t%s" % item.key)

    except Exception as errors:
        print(errors)

    bucket = input('\nPlease type in the name of the bucket you wish to choose a file from: ')
    picture = input('\nPlease type in the name of the image you uploaded: ')

    # Indentation matters // not really

    # create the index page
    def createindex():
        htmlfile = open("index.html", "w+")

        htmlfile.write('<img src="https://s3-eu-west-1.amazonaws.com/' + bucket + '/' + picture + '"/>' + '<br />'
                                                                                                          '<a href = "https://s3-eu-west-1.amazonaws.com/' + bucket + '/' + picture + '">' +
                       'Link to image' + '</a>')
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
            print(10 * '-', 'index uploaded', 10 * '-', '/n')

            progress(10)

            output = subprocess.run(cmd_scp, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(output)

            cmd = "ssh -i devops.pem ec2-user@" + instance.public_ip_address + " 'cd /usr/share/nginx/html; " \
                                                                               "sudo rm -f index.html; " \
                                                                               "cd ~; " \
                                                                               "sudo mv index.html /usr/share/" \
                                                                               "nginx/html/index.html'"
            progress(10)

            output = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(output)

            print(5 * '-', 'opening in the best web browser', 5 * '-', '/n')
            webbrowser.open_new(instance.public_ip_address)

    except Exception as error:
        print(error)


# Define a main() function
def main():
    add_file()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
