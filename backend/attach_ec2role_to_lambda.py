import boto3
import json


def attach_hopper_ec2_role_to_lambda():
    client = boto3.client('iam')
    policy = client.get_role_policy(RoleName='backend-dev-ZappaLambdaExecutionRole', PolicyName='zappa-permissions')
    pj = policy['PolicyDocument']
    pj['Statement'].append({
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": "arn:aws:iam::405696771294:role/hopper-ec2"
    })
    response = client.put_role_policy(RoleName='backend-dev-ZappaLambdaExecutionRole',PolicyName='zappa-permissions',PolicyDocument=json.dumps(pj))


if __name__ == "__main__":
    attach_hopper_ec2_role_to_lambda()