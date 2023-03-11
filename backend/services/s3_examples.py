import logging
import boto3
from botocore.exceptions import ClientError



def list_buckets():
    session = boto3.Session(profile_name='lamarr')
    s3 = session.client('s3')
    response = s3.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    session = boto3.Session(profile_name='lamarr')
    try:
        if region is None:
            s3_client = session.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = session.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True



res = input("List buckets - 1, Create bucket - 2, Quit - q: ")

while res != "q":
    if res == '1':
        list_buckets()
    elif res == "2":
        buck_name = input("Please enter unique bucket name: ")
        create_bucket(buck_name, "us-east-2")
    
    res = input("List buckets - 1, Create bucket - 2, Quit - q: ")
