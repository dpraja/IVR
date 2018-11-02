from sqlwrapper import gensql,dbget,dbput
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

    r = requests.post('https://ivrinfocuit.herokuapp.com/get_aws_keys')
    
    print (r.json(),type(r.json()))

    res = r.json()

    print(res)
    
    key_id = res['Returnvalue'][0]['img_s3_keyid']
    secret_access_key = res['Returnvalue'][0]['img_s3_key']

    print(key_id, secret_access_key)
    
    s3 = boto3.resource('s3',region_name='us-east-1',aws_access_key_id=key_id,
                        aws_secret_access_key=secret_access_key)

    s3.Bucket(bucket).put_object(Key=key,Body=image)
    
    url = client.generate_presigned_url('get_object',Params = {'Bucket':bucket,'Key':key})
    print(url)

    return (json.dumps({"Status":"Success","Message":"Image Uploaded in S3 Bucket","url":url}))


def get_aws_keys(request):

    tb_id = {"tb_id":1}

    res = json.loads(gensql('select','aws_keys','*',tb_id))
    
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success",
                      "Status_Code": "200","Returnvalue":res },indent=2))
    
