
from botocore.client import Config
import boto3
import json

def upload_file(request):
    print (type(request.files))
    bucket = 'image-upload-rekognition'
    key = 'baladp.jpg'
    image = request.files['Image']
    name = image.name
    print (name)
    client = boto3.client('s3')
    s3 = boto3.resource('s3')

    s3.Bucket(bucket).put_object(Key=key,Body=image)
    url = client.generate_presigned_url('get_object',Params = {'Bucket':bucket,'Key':key})
    print(url)
    return (json.dumps({"Status":"Success","Message":"Image Uploaded in S3 Bucket","url":url}))
        
