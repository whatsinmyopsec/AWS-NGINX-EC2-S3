import os

import boto3

# Declaring S3 variable
s3 = boto3.resource("s3")


# Uploads a file to a bucket
def put_bucket():
    for bucket in s3.buckets.all():
        print('\nList of buckets:')
        print(bucket.name)

    bucket = input('\nPlease type in the name of the bucket you wish to upload to: ')

    #
    source = os.getcwd()
    print('Files in folder: \n ')
    for fn in os.listdir(source):
        if os.path.isfile(fn):
            print(fn)
    file = input('\nPlease type in the file you wish to upload to ' + bucket + ': ')

    try:
        response = s3.Object(bucket, file).put(Body=open(file, 'rb'))
        print('\nFile has been uploaded successfully\n' + response)

    except Exception as error:
        print(error)

    # Adding Public Read Only Access
    try:
        object_acl = s3.ObjectAcl(bucket, file).put(ACL='public-read')
        print('\nAdded Public Read Only Access to ' + file + object_acl)
    except Exception as error:
        print(error)


# Define a main() function
def main():
    put_bucket()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
