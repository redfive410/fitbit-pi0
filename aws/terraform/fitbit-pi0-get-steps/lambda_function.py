import os
import sys
import boto3
import datetime

parent_dir = os.path.abspath(os.path.dirname(__file__))
lib_dir = os.path.join(parent_dir, 'lib')

sys.path.append(lib_dir)

import fitbit

class PST(datetime.tzinfo):
    def utcoffset(self, dt):
      return datetime.timedelta(hours=-8)

    def dst(self, dt):
        return datetime.timedelta(0)

def update_tokens(token):
    print("update_tokens start...")
    ssm = boto3.client('ssm', 'us-west-2')
    response = ssm.get_parameter(Name='/fitbit/access_token',WithDecryption=True)
    access_token = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/fitbit/refresh_token',WithDecryption=True)
    refresh_token = response['Parameter']['Value']

    if (token['access_token'] != access_token or token['refresh_token'] != refresh_token):
        print("Updating OAuth Tokens...")
        ssm.put_parameter(Name='/fitbit/access_token',Value=token['access_token'],Type='SecureString',Overwrite=True)
        ssm.put_parameter(Name='/fitbit/refresh_token',Value=token['refresh_token'],Type='SecureString',Overwrite=True)

def lambda_handler(event, context):
    ssm = boto3.client('ssm', 'us-west-2')
    response = ssm.get_parameter(Name='/fitbit/consumer_key',WithDecryption=True)
    consumer_key = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/fitbit/consumer_secret',WithDecryption=True)
    consumer_secret = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/fitbit/access_token',WithDecryption=True)
    access_token = response['Parameter']['Value']

    response = ssm.get_parameter(Name='/fitbit/refresh_token',WithDecryption=True)
    refresh_token = response['Parameter']['Value']

    client = fitbit.Fitbit(consumer_key,
                           consumer_secret,
                           access_token=access_token,
                           refresh_token=refresh_token,
                           refresh_cb=update_tokens)

    print(client.activities_daily_goal())

    now = datetime.datetime.now(PST())
    print(now)

    end_time = now.strftime("%H:%M")
    response = client.intraday_time_series('activities/steps',
                                            detail_level='15min',
                                            start_time="00:00",
                                            end_time=end_time)
    steps = response['activities-steps'][0]['value']
    print(steps)

    return steps
