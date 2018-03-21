#!/usr/bin/python3
import boto3
import json

if __name__ == "__main__":
    print('Hello Pi0')

    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='fitbit-pi0-get-steps'
    )

    steps = response['Payload'].read()
    print(steps)

    print('Goodbye Pi0')
