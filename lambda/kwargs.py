import json
import boto3


# Bedrock client used to interact with APIs around models
bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1'
)

# Bedrock Runtime client used to invoke and question the models
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def lambda_handler(event,context):
    
    prompt="tell me about SpaceX"
    
    
    kwargs={
     "modelId": "meta.llama3-8b-instruct-v1:0",
     "contentType": "application/json",
     "accept": "application/json",
     "body": "{\"prompt\":\"Human:" +prompt + "\",\"max_gen_len\":512,\"temperature\":0.5,\"top_p\":0.9}"
    }
    response=bedrock_runtime.invoke_model(**kwargs)
    response_json=json.loads(response.get('body').read())
    
    return {
        'statusCode': 200,
        'body': json.dumps(response_json)
    }
    
    