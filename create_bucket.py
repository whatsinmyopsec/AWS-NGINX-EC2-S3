import time

import boto3

# Declaring S3 variable
s3 = boto3.resource("s3")


# Creates a new bucket
def create_bucket():
    print('\nCreating a new bucket')
    print(21 * "-")
    time.sleep(1)
    s3 = boto3.client('s3')
    # get bucket name input from user
    bucketname = input("Please Enter Bucket name (unique): ")

    # try/except so the script will not crash
    try:
        # create bucket with location in Ireland
        response = s3.create_bucket(
            Bucket=bucketname,
            ACL='public-read',
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print(response)

        # if bucket successfully created then print message for user
        print("creating bucket successful")
        print(response)
    except Exception as error:
        print(error)

    return bucketname


# Define a main() function
def main():
    create_bucket()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
