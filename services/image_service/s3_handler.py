import os
import re
import uuid
from urllib.parse import unquote_plus

import boto3
from PIL import Image
from aws_lambda_powertools import Logger, Tracer

s3_client = boto3.client('s3')
logger = Logger()
tracer = Tracer()

THUMBNAIL_SIZE = 320, 180


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def resize(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        # ディレクトリの場合には何もしない
        if key.endswith('/'):
            return

        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        resized_path = '/tmp/resized-{}'.format(tmpkey)

        filename = key.split('/')[-1]
        dirname = re.sub(filename + '$', '', key)
        basename, ext = os.path.splitext(filename)
        resized_key = '{}{}_thumb{}'.format(dirname, basename, ext)

        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, resized_path)
        s3_client.upload_file(resized_path, os.environ['RESIZE_BUCKET_NAME'], resized_key)
        logger.info('サムネイルを生成しました({})'.format(resized_key))


@tracer.capture_method
def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(THUMBNAIL_SIZE)
        image.save(resized_path)
