import json
import os
import unittest
from unittest.mock import patch

import boto3
from moto import mock_sqs

from tests.common import aws_resource, test_utils


@mock_sqs
class TestApigwHandler(unittest.TestCase):
    def setUp(self):
        aws_resource.create_sqs_queue(self)
        self.env = patch.dict('os.environ', {
            'QUEUE_URL': self._queue_url,
        })

    def tearDown(self):
        aws_resource.delete_sqs_queue(self)

    def test_hello(self):
        with self.env:
            from services.sample_service import apigw_handler

            sqs_resource = boto3.resource('sqs')
            queue = sqs_resource.Queue(os.environ['QUEUE_URL'])

            with open('tests/sample_service/apigw_event.json', encoding='utf-8', mode='r') as f:
                apigw_event = json.load(f)

            response = apigw_handler.hello(apigw_event, test_utils.mock_context())
            self.assertEqual(response['statusCode'], 200)

            messages = queue.receive_messages(QueueUrl=os.environ['QUEUE_URL'])
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].body, "これはテストです")
