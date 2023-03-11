from flask import current_app
import boto3
from .hopper_utils import (
    get_account_credentials,
    get_boto3_session,
    find_instance_by_name,
    find_db_instance_by_name,
    check_mysql_sg_only_access,
    check_sg_ingress,
    check_cidr_open_all,
    check_all_ports_open,

)
from .base_service import _get, get_accounts


ACCOUNTS = get_accounts()
LAB_ID = "lab1"


def check_ssh_security():
    students = []
    for account in ACCOUNTS:
        ec2 = _get('arn:aws:iam::405696771294:role/hopper-ec2',
                   f'arn:aws:iam::{account}:role/allow-assume-EC2-role-in-Lamarr1', 'ec2')
        instance = find_instance_by_name(ec2, LAB_ID)
        message = ''
        student = ''
        is_success = True
        if instance == None:
            message = f'No EC2 instance instance found by name: {LAB_ID}'

        for key_pair in ec2.describe_key_pairs()['KeyPairs']:
            if 'student' in key_pair['KeyName'].lower():
                student = key_pair['KeyName']

        if len(instance.describe_security_groups()['SecurityGroups']) == 0:
            is_success = True
            message = 'No security group found!'

        for sg in instance.describe_security_groups()['SecurityGroups']:
            if 'ssh' in sg['Description'].lower():
                for ip_range in sg['IpPermissions'][0]['IpRanges']:
                    if ip_range['CidrIp'] == '0.0.0.0/0' or ip_range['CidrIp'] == '::/0':
                        message = 'SSH CidrIp is accessable for public'
                        is_success = False
                    else:
                        is_success = True
                        message = 'Not open to public!'
        students.append(
            {'name': student, 'message': message, 'is_success': is_success})
    return students
