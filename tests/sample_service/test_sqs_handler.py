import json
import os
import unittest
from unittest.mock import patch

import boto3
from moto import mock_sqs, mock_dynamodb2

from tests.common import aws_resource, test_utils


@mock_sqs
@mock_dynamodb2
class TestSqsHandler(unittest.TestCase):
    def setUp(self):
        aws_resource.create_sqs_queue(self)
        aws_resource.create_dynamodb_table(self)
        self.env = patch.dict('os.environ', {
            'QUEUE_URL': self._queue_url,
            'TABLE_NAME': self._table_name,
        })

    def tearDown(self):
        aws_resource.delete_sqs_queue(self)
        aws_resource.delete_dynamodb_table(self)

    def test_save_table(self):
        with self.env:
            from services.sample_service import sqs_handler

            dynamodb_sample_table_tbl = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

            with open('tests/sample_service/sqs_event.json', encoding='utf-8', mode='r') as f:
                sqs_event = json.load(f)

            sqs_handler.save_table(sqs_event, test_utils.mock_context())

            items = dynamodb_sample_table_tbl.scan()['Items']
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]['message'], "これはテストです")
