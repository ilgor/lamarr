from flask import current_app
import boto3
import json
import time
from .base_service import get_accounts, _get


ACCOUNTS = get_accounts()


def initial_setup():
    for account in ACCOUNTS:
        ec2 = _get('arn:aws:iam::405696771294:role/hopper-ec2',
                   f'arn:aws:iam::{account}:role/allow-assume-EC2-role-in-Lamarr', 'ec2')
        try:
            ec2.describe_key_pairs(KeyNames=['DemoKey', ],)
        except Exception as e:
            keypair = ec2.create_key_pair(KeyName='DemoKey')

        cf = _get('arn:aws:iam::405696771294:role/hopper-cf',
                  f'arn:aws:iam::{account}:role/allow-assume-CF-role-in-Lamarr', 'cloudformation')
        try:
            r1 = cf.describe_stacks(StackName='InitialSetup')['Stacks'][0]
            r2 = cf.delete_stack(StackName='InitialSetup')[
                'ResponseMetadata']['HTTPStatusCode']
            time.sleep(3)
            print(f'Stack Deletion Status: {r2}')
        except Exception as e:
            pass

        with current_app.open_resource('services/params.json') as f:
            lo_json_data = f.read()
            la_parameters_data = json.loads(lo_json_data)

            print("Loading parameters from parameters file:")
            lc_template_url = ""
            la_create_stack_parameters = []
            for lc_key in la_parameters_data.keys():
                if lc_key == "TemplateUrl":
                    lc_template_url = la_parameters_data["TemplateUrl"]
                elif lc_key == "StackName" or lc_key == "RegionId":
                    pass
                else:
                    print(lc_key + " - " + la_parameters_data[lc_key])
                    la_create_stack_parameters.append(
                        {"ParameterKey": lc_key, "ParameterValue": la_parameters_data[lc_key]})

            stack_result = cf.create_stack(
                StackName=la_parameters_data['StackName'], DisableRollback=True, TemplateURL=la_parameters_data['TemplateUrl'], Parameters=la_create_stack_parameters, Capabilities=["CAPABILITY_IAM"])


def get_sqs():
    attrs = []
    for account in ACCOUNTS:
        result = _get('arn:aws:iam::405696771294:role/hopper',
                      f'arn:aws:iam::{account}:role/allow-assume-SQS-role-in-Lamarr', 'sqs')

        temp = []
        res = result.list_queues()

        if res.get('QueueUrls') != None:
            urls = res['QueueUrls']
            for url in urls:
                try:
                    res = result.get_queue_attributes(
                        QueueUrl=url, AttributeNames=['QueueArn'])
                    temp.append(
                        {'url': url, 'arn': res['Attributes']['QueueArn'], 'in_progress': False})
                except:
                    temp.append({'url': url, 'arn': '', 'in_progress': True})

        attrs.append({'account': account, 'data': temp})

    return {'name': 'SQS', 'attrs': attrs}


def create_sqs(name, account):
    client = _get('arn:aws:iam::405696771294:role/hopper',
                  f'arn:aws:iam::{account}:role/allow-assume-SQS-role-in-Lamarr', 'sqs')
    client.create_queue(QueueName=name)


def delete_sqs(url):
    account = url.replace(
        'https://us-east-2.queue.amazonaws.com/', '').split('/')[0]
    client = _get('arn:aws:iam::405696771294:role/hopper',
                  f'arn:aws:iam::{account}:role/allow-assume-SQS-role-in-Lamarr', 'sqs')
    client.delete_queue(QueueUrl=url)
