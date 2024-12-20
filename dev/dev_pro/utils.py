import logging
import os

import boto3
from botocore.exceptions import ClientError
# import settings
# from dev import  settings

# def create_bucket(bucket_name, region=None):
#     """Create an S3 bucket in a specified region
#
#     If a region is not specified, the bucket is created in the S3 default
#     region (us-east-1).
#
#     :param bucket_name: Bucket to create
#     :param region: String region to create bucket in, e.g., 'us-west-2'
#     :return: True if bucket created, else False
#     """
#
#     # Create bucket
#     try:
#         if region is None:
#             s3_client = boto3.client('s3')
#             s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
#         else:
#             s3_client = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                                      region_name=settings.AWS_S3_REGION_NAME
#                                      )
#             location = {'LocationConstraint': region}
#             s3_client.create_bucket(Bucket=bucket_name,
#                                     CreateBucketConfiguration=location)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True
#
#
# # create_bucket("samplebucketautomac2",'ap-south-1')
#
#






def upload_file(file_name, bucket, object_name=None,region=None):
    print('in upload_file')
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id='AKIAVRUVWVFCSQBD3LNO',
                                         aws_secret_access_key='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',
                                         region_name='ap-south-1'
                                         )
    # Set metadata for the uploaded file
    extra_args = {
        "ContentType": "application/pdf",
        "ContentDisposition": "inline"
    }
    print('s3_client',s3_client)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=extra_args)  #ExtraArgs=extra_args
    except ClientError as e:
        logging.error(e)
        return False
    print('response',response)
    return object_name

# upload_file("test_files/jiraya.png", "samplebucketautomac2", "ji.img",


