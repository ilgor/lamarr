import json
import boto3


def get_accounts():
    return ['404771415876', '624041382079', '337731452564']

def _get(hopper_role_arn, lamarr_role_arn, service):
    client_hopper = boto3.client('sts')
    response = client_hopper.assume_role(RoleArn=hopper_role_arn, RoleSessionName='assuming-hopper')
    credentials = response['Credentials']

    client_lamarr = boto3.client(
        'sts',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    response_lamarr = client_lamarr.assume_role(
        RoleArn=lamarr_role_arn, RoleSessionName='assuming-lamarr')
    credentials_hopper = response_lamarr['Credentials']

    return boto3.client(
        service,
        aws_access_key_id=credentials_hopper['AccessKeyId'],
        aws_secret_access_key=credentials_hopper['SecretAccessKey'],
        aws_session_token=credentials_hopper['SessionToken'],
    )
