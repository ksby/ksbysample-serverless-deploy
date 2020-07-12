import datetime
import os

import boto3
from aws_lambda_powertools import Logger, Tracer

dynamodb_sample_table_tbl = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def save_table(event, context):
    logger.debug(event)

    for record in event['Records']:
        dynamodb_sample_table_tbl.put_item(
            Item={
                'timestamp': datetime.datetime.now().isoformat(),
                'message': record['body']
            }
        )
