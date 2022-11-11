import json
import urllib.parse
import boto3
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = os.environ['sns_topic_arn']

def create_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    eventname = event['Records'][0]['eventName']
    sns_message = str("A New file has been Uploaded to Your Bucket \n\n BUCKET NAME: "+ bucket +"\n\n FILE NAME: " + key + "\n\n OPERATION: " + eventname + "\n\n")
    try:
        if eventname == "ObjectCreated:Put":
            response = s3.get_object(Bucket=bucket, Key=key)
            sns_message += str("FILE CONTENT TYPE: " + str(response['ContentType']))
        subject= "S3 Bucket[" + bucket + "] Event[" + eventname + "]"
        url = create_presigned_url(bucket, key)
        sns_response = sns.publish(
            TargetArn=sns_topic_arn,
            Message= str(sns_message + "\n\nFILE URL: " + url),
            Subject= str(subject)
        )
    except Exception as e:
        print(e)
        print('Error fetching object {} from bucket {}. Make sure the object exists in the bucket and is in the same region as this function.'.format(key, bucket))
        raise e
