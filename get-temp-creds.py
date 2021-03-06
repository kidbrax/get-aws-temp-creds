#!/usr/bin/env python3

# This script will read creds for a given profile from your ~/.aws/credentials file
# and then get temp session creds and then write those back out to your ~/.aws/credentials file
# with a '-temp' extension on the profile name

import argparse
import configparser
import os
import sys
import boto3

def get_permanent_creds(profile_name):
    file_object = open(credentials_path, 'r')
    print("Reading permanent creds for {}".format(profile_name))
    creds_parser.read_file(file_object)
    key = creds_parser[profile_name]['aws_access_key_id']
    secret = creds_parser[profile_name]['aws_secret_access_key']
    return key, secret

def get_mfa_arn(profile_name):
    print("Getting MFA ARN for {}".format(profile_name))
    file_object = open('/Users/braxtonbeyer/.aws/config', 'r')
    config_parser.read_file(file_object)
    return config_parser['profile '+profile_name]['mfa_serial']

def write_temp_creds(profile_name, temp_creds):
    temp_profile_name = profile_name+'-temp'
    print('Writing temp creds to {}'.format(temp_profile_name))

    creds_parser[temp_profile_name] = {}
    creds_parser[temp_profile_name]['aws_access_key_id'] = temp_creds['AccessKeyId']
    creds_parser[temp_profile_name]['aws_secret_access_key'] = temp_creds['SecretAccessKey']
    creds_parser[temp_profile_name]['aws_session_token'] = temp_creds['SessionToken']
    creds_parser[temp_profile_name]['expires'] = "{}".format(temp_creds['Expiration'])
    with open(credentials_path, 'w') as config_file:
        creds_parser.write(config_file)

    print(
        'Temp creds have been written to ~/.aws/credentials. They will expire at {}'
        .format(temp_creds['Expiration'])
    )

def get_temp_creds(profile_name, aws_key, aws_secret, mfa_arn):
    sts = boto3.client(
        'sts',
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )
    mfa_token = input('Enter the MFA token: ')
    # print('MFA token is {}'.format(mfa_token))

    temp_creds = sts.get_session_token(
        SerialNumber=mfa_arn,
        TokenCode=mfa_token
    )
    # print(temp_creds['Credentials'])

    write_temp_creds(profile_name, temp_creds['Credentials'])


parser = argparse.ArgumentParser(description='Update your aws/.credentials file with a temp profile for your session.')
parser.add_argument(
    'profile_name',
    type=str,
    help='The name of the profile you want to use to get your session token'
)
args = parser.parse_args()

credentials_path = "{}/.aws/credentials".format(os.environ['HOME'])
creds_parser = configparser.ConfigParser()
config_parser = configparser.ConfigParser()
aws_key, aws_secret = get_permanent_creds(args.profile_name)
mfa_arn = get_mfa_arn(args.profile_name)

get_temp_creds(args.profile_name, aws_key, aws_secret, mfa_arn)
