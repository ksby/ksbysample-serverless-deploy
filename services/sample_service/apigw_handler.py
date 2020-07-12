import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

sqs_client = boto3.client('sqs')
logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def hello(event, context):
    logger.debug(event)

    response = sqs_client.send_message(
        QueueUrl=os.environ['QUEUE_URL'],
        MessageBody=event['queryStringParameters']['message']
    )

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
