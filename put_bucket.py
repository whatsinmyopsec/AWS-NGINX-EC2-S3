import os
import pprint

import boto3

# Declaring S3 variable
s3 = boto3.resource("s3")


# Uploads a file to a bucket
def put_bucket():
    for bucket in s3.buckets.all():
        print('\nList of buckets:')
        print(bucket.name)

    bucket = input('\nPlease type in the name of the bucket you wish to upload to: ')

    # List files in current directory
    source = os.getcwd()
    print('Files in folder: \n ')
    for fn in os.listdir(source):
        if os.path.isfile(fn):
            print(fn)
    image = input('\nPlease type in the image you wish to upload to ' + bucket + ': ')

    try:
        response = s3.Object(bucket, image).put(Body=open(image, 'rb'), ContentType='i')
        pprint.pprint('\nFile has been uploaded successfully\n' + response)

    except Exception as error:
        print(error)

    # Adding Public Read Only Access
    try:
        object_acl = s3.ObjectAcl(bucket, image).put(ACL='public-read')
        print('\nAdded Public Read Only Access to ' + image + object_acl)
    except Exception as error:
        print(error)


# Define a main() function
def main():
    put_bucket()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
