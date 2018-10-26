# Devops-Assign-1

This is a project that uses Python 3 and the Boto library to start Amazon Web Services(AWS) (EC2)instances and (S3)buckets. 
There are also scripts that start services like Nginx servers on remote instances.

## Pre-requisites

To get started, you will need to have the following requirements setup

- python 3 or greater
- ssh/scp installed and allowed access to the internet on port 22
- An AWS account with RSA public/private key setup see http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html for more information
- You will need your own pem file
- And security groupid with ssh and http
- You will need your Boto library configured to interact with AWS see http://boto3.readthedocs.io/en/latest/guide/configuration.html for more information

# Starting the App
- git clone this repo
- cd to the directory
- make sure to copy or move your pem file to here
- pip3 install -r requirements.txt
- python3 menu.py
