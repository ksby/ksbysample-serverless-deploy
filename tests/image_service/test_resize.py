import json
import os
import unittest
from unittest.mock import patch

import boto3
from moto import mock_s3

from tests.common import aws_resource, test_utils


@mock_s3
class TestResizeService(unittest.TestCase):

    def setUp(self):
        aws_resource.create_s3_bucket(self)
        self.env = patch.dict('os.environ', {
            'UPLOAD_BUCKET_NAME': self._upload_bucket_name,
            'RESIZE_BUCKET_NAME': self._resize_bucket_name
        })

    def tearDown(self):
        aws_resource.delete_s3_bucket(self)

    def test_resize(self):
        with self.env:
            from services.image_service import s3_handler

            s3_client = boto3.client('s3')
            s3_client.upload_file('tests/image_service/sample.jpg',
                                  os.environ['UPLOAD_BUCKET_NAME'], 'sample.jpg')

            with open('tests/image_service/s3_event.json', 'r') as f:
                event = json.load(f)

            s3_handler.resize(event, test_utils.mock_context())

            thumb_object = s3_client.get_object(Bucket=os.environ['RESIZE_BUCKET_NAME'],
                                                Key='sample_thumb.jpg')
            self.assertEqual(thumb_object['ResponseMetadata']['HTTPStatusCode'], 200)
            self.assertGreater(int(thumb_object['ResponseMetadata']['HTTPHeaders']['content-length']), 0)

            # 生成されたサムネイル画像をダウンロードすることも出来る（実際に作成される）
            # s3_client.download_file(TestResizeService.RESIZE_BUCKET, 'sample_thumb.jpg',
            #                         'tests/sample_thumb.jpg')
