import logging
import boto3
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_ROLE_NAME = 'hopper-test-agent'


def check_wrong_port_open(rule, wrongport):
    logger.info(rule)
    if rule['ToPort'] == int(wrongport) or rule['FromPort'] == int(wrongport):
        logger.info('Wrong port detected')
        return True
    else:
        logger.info('Wrong port NOT detected')
        return False


# Check if any rule has wide open ports.
def check_all_ports_open(rule):
    all_ports = (rule.get('FromPort') ==
                 0 and rule.get('ToPort') in [65535, 0])
    all_access = (rule.get('IpProtocol') == '-1')
    return all_ports or all_access


# Check if a rule has wide open IP access.
def check_cidr_open_all(rule):
    for ip_range in rule['IpRanges']:
        if ip_range['CidrIp'] == '0.0.0.0/0':
            return True
    return False


# Check if a rule (usually wide open ports) is assigned to a SG not a CidrIp.
def check_sg_ingress(rule):
    for sg in rule.get('UserIdGroupPairs'):
        if sg['GroupId']:
            return True
        else:
            return False


# Mysql RDS access
def check_mysql_sg_only_access(rule):
    if rule.get('FromPort') == 3306 and rule.get('ToPort') == 3306:
        if not check_sg_ingress(rule) or check_cidr_open_all(rule):
            return False
        else:
            return True


def find_db_instance_by_name(rds, name):
    db_instances = rds.describe_db_instances()['DBInstances']
    for instance in db_instances:
        if instance['DBName'] == 'wp01' or instance['DBInstanceIdentifier'] == 'wp01':
            return instance


def find_instance_by_name(ec2, name):
    tags = ec2.describe_tags()['Tags']
    for tag in tags:
        if tag['Key'] == 'Name' and tag['Value'] == 'lab1':
            return ec2
    return None

# Returns an authorized boto3 client


def get_boto3_session(credentials, region):
    try:
        session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=region
        )
        return session
    except ClientError as e:
        logging.critical(f"Failure getting boto3 session: {e}")
        raise e


def get_account_credentials(account_id):
    role_name = DEFAULT_ROLE_NAME
    sts_connection = boto3.client('sts')
    other_account = sts_connection.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName=role_name
    )
    return other_account['Credentials']
