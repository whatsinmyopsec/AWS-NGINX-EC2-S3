import json

import boto3

# Declaring S3 variable
s3 = boto3.resource("s3")


# Creates a new bucket
def create_bucket():
    print('\nCreating a new bucket')
    # Ask the user to give the new bucket a name
    bucketname = input('Please give your new bucket a unique name: ')

    # try/except so the script will not crash
    try:
        response = s3.create_bucket(
            Bucket=bucketname,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print(response)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::" + bucketname + "/*"]
                }
            ]
        }
        # converting to a json format
        policy = json.dumps(policy)
        # adding policy to newly created bucket
        boto3.client('s3').put_bucket_policy(Bucket=bucketname, Policy=policy)
        print("Bucket given read permissions")
    except Exception as error:
        print(error)


# Define a main() function
def main():
    create_bucket()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
