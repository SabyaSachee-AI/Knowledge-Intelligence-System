import boto3
from botocore.exceptions import ClientError 
from app.config import config

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY
        )
        self.bucket_name = config.AWS_BUCKET_NAME

    def upload_file(self, file_obj, filename):
        try:
            self.s3.upload_fileobj(file_obj, self.bucket_name, filename)
            return True
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False

    def get_file(self, filename):
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=filename)
            return response['Body']
        except ClientError as e:
            print(f"Error retrieving file: {e}")
            return None
        

        
