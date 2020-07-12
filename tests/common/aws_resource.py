import os

import boto3

UPLOAD_BUCKET_NAME = 'ksbysample-upload-bucket'
RESIZE_BUCKET_NAME = 'ksbysample-resize-bucket'
QUEUE_NAME = 'sample-queue-test'
TABLE_NAME = 'sample-table-test'


def create_s3_bucket(self):
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=UPLOAD_BUCKET_NAME)
    s3_client.create_bucket(Bucket=RESIZE_BUCKET_NAME)
    self._upload_bucket_name = UPLOAD_BUCKET_NAME
    self._resize_bucket_name = RESIZE_BUCKET_NAME


def create_sqs_queue(self):
    sqs_client = boto3.client('sqs')
    response = sqs_client.create_queue(QueueName=QUEUE_NAME)
    self._queue_url = response['QueueUrl']


def create_dynamodb_table(self):
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_client.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {
                "AttributeName": "timestamp", "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "timestamp", "KeyType": "HASH"
            }
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    self._table_name = TABLE_NAME


def delete_s3_bucket(self):
    s3 = boto3.resource('s3')
    upload_bucket = s3.Bucket(UPLOAD_BUCKET_NAME)
    upload_bucket.objects.all().delete()
    upload_bucket.delete()
    resize_bucket = s3.Bucket(RESIZE_BUCKET_NAME)
    resize_bucket.objects.all().delete()
    resize_bucket.delete()


def delete_sqs_queue(self):
    with self.env:
        sqs_client = boto3.client('sqs')
        sqs_client.delete_queue(
            QueueUrl=os.environ['QUEUE_URL']
        )


def delete_dynamodb_table(self):
    with self.env:
        dynamodb_client = boto3.client('dynamodb')
        dynamodb_client.delete_table(TableName=os.environ['TABLE_NAME'])
